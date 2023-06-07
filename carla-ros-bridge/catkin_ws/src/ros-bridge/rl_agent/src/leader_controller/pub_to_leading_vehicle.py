#!/usr/bin/env python

"""
Subscribe Leading vehicle's velocity and acceleration and publish control command to the following vehicle
"""
import sys
import datetime
import numpy
import rospy
import numpy as np
import math
import rospkg
from ackermann_msgs.msg import AckermannDrive  # pylint: disable=import-error
from carla_msgs.msg import CarlaEgoVehicleStatus  # pylint: disable=no-name-in-module,import-error
from carla_msgs.msg import CarlaEgoVehicleControl  # pylint: disable=no-name-in-module,import-error
from carla_msgs.msg import CarlaEgoVehicleInfo  # pylint: disable=no-name-in-module,import-error
from carla_ackermann_msgs.msg import EgoVehicleControlInfo  # pylint: disable=no-name-in-module,import-error
from carla_msgs.msg import CarlaCollisionEvent  
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Pose
import csv
import argparse
from carla_ackermann_control import carla_control_physics as phys
from simple_pid import PID
import rospkg


rospack = rospkg.RosPack()
current_path = rospack.get_path('rl_agent')



# get config 
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--leader_profile", help="Which leader speed profile will be used for evaluation.", type=str, default="Napoli")
args = parser.parse_args()

leader_speed = args.leader_profile
vl = []

if leader_speed == "napoli":
    with open(current_path + "/src/leader_controller/evaluation_leader_profile/Napoli/full_napoli_datasets.csv", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            vl_data = row[2]       
            vl.append(vl_data)
elif leader_speed == "self_defined"
    with open(current_path + "/src/leader_controller/evaluation_leader_profile/self_defined_leader.csv", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            vl_data = row[2]       
            vl.append(vl_data)
elif leader_speed == "ngsim":
    with open(current_path + "/src/leader_controller/evaluation_leader_profile/NGSIM/data_veh2159.csv", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            vl_data = row[2]       
            vl.append(vl_data)    
else:
    raise NotImplementedError("Cannot find the speed profile of the leader.")


class CarlaAckermanControl(object):
    def __init__(self):
        self.control = CarlaEgoVehicleControl()
        self.rate = rospy.Rate(10)
        self.NN_INPUT = np.matrix([[0.0],[0.0],[0.0]])
        self.output_throttle = 0.0
        self.output_brake =  0.0
        self.Veh_Velocity = 0.0
        self.Veh_Accleration = 0.0
        self.yaw_path = 0.0
        self.FC_w1 = np.array([[-4.0420e-02,  8.1333e-01,  4.6500e-01],
        [-6.3612e-01,  7.0163e-01, -1.8089e-01],
        [-7.0203e-01,  6.3108e-01, -1.9478e-01],
        [ 8.5185e-01, -6.5471e-01, -1.2376e-02],
        [ 1.0560e+00, -8.0366e-01,  5.0712e-02],
        [ 5.2281e-02, -3.6304e-01,  8.7340e-02],
        [-1.6747e+01, -6.5886e+00, -9.6849e-01],
        [ 6.4617e-01, -8.2533e-01,  5.4079e-01]])

        self.FC_w2 = np.array([[ 0.4874,  1.1844, -0.8867, -0.8287, -0.7548,  1.2879,  1.2941,  0.6623],
        [-0.2216, -1.9335,  0.3573,  0.5107,  0.4946,  0.5591, -5.7986,  0.4116],
        [ 0.4682, -2.7579, -0.6543, -0.9467, -1.3642,  0.4208, -2.7700, -0.0477],
        [ 0.2533, -0.1550,  1.2005,  0.8561,  1.1621, -0.5143, -1.7282,  0.0214],
        [ 0.5687, -0.4565, -1.4163, -0.2861, -0.5806, -2.1951, -1.1219, -1.6048],
        [-0.4492, -0.9092, -0.8107,  0.6467,  1.1006,  0.4098, -2.5963,  0.4906],
        [ 0.3386, -0.0514, -0.3039, -0.0756, -0.2827, -1.1903,  8.6665, -0.8114],
        [-0.2841,  0.5537,  2.0911,  0.9557,  1.5246, -0.2759, -3.4949,  0.1435]])
	
        self.FC_w3 = np.array([[-1.6370,  0.8193,  1.8599,  0.2527, -0.3269,  2.1283, -0.6340,  0.5806],
        [ 1.7897, -0.9015,  2.3927, -0.9361,  2.0672, -5.5530,  1.8623, -2.4810]])
 
        self.FC_b1 = np.array([ 0.0672, -0.1978,  0.4918,  0.2788,  0.1029,  1.5478,  0.2604,  0.2861]).reshape(8,1)


        self.FC_b2 = np.array([-0.2506,  0.0641,  1.0010, -0.3147,  0.2478, -0.0566,  1.4796,  0.0864]).reshape(8,1)
        self.FC_b3 = np.array([-1.8596, -0.3640]).reshape(2,1)

        self.sub_vehicle_velocity = rospy.Subscriber("/carla/hero1/vehicle_status",CarlaEgoVehicleStatus,self.leading_velocity_callback,queue_size = 10)
        self.sub_leading_vehicle_position = rospy.Subscriber("/carla/hero1/odometry",Odometry,self.leading_vehicle_position_callback,queue_size = 10)
        
        self.sub_following_vehicle_position = rospy.Subscriber("/carla/hero2/odometry",Odometry,self.following_vehicle_position_callback,queue_size = 10)
        self.sub_collision = rospy.Subscriber("/carla/hero2/collision", CarlaCollisionEvent, self.following_vehicle_collision_callback,queue_size = 10)
        self.sub_respawn = rospy.Publisher("/carla/hero1/control/set_transform", Pose, self.respawn_callback,queue_size = 10)
        self.respawn = False
        self.collision_other_actor_id = 0
        self.collision_list=[]





    def respawn_callback(self, data):
        if data != None:
            self.respawn = True

    
    def leading_vehicle_position_callback(self,data):
         self.Lead_Veh_Position_x = data.pose.pose.position.x
         self.Lead_Veh_Position_y = data.pose.pose.position.y
       
    def following_vehicle_position_callback(self,data):      
        self.Follow_Veh_Position_y = data.pose.pose.position.y
        self.Follow_Veh_Position_x = data.pose.pose.position.x

    def following_vehicle_collision_callback(self, data):
        self.collision_other_actor_id = data.other_actor_id
        self.collision_list.append(self.collision_other_actor_id)


        
    def leading_velocity_callback(self,data):
        self.Veh_Velocity = data.velocity
        self.Veh_Accleration = data.acceleration.linear.x
        self.yaw = data.orientation.y        
    def from_velocity_to_gas(self):
        self.FC_output1_layer = np.maximum((np.dot(self.FC_w1,self.NN_INPUT) + self.FC_b1),0.0)
        self.FC_output2_layer = np.maximum((np.dot(self.FC_w2,self.FC_output1_layer) + self.FC_b2),0.0)
        self.FC_output3_layer =np.dot(self.FC_w3,self.FC_output2_layer)+self.FC_b3
        
        self.output_throttle = 1.0/(1.0 + np.exp(-(self.FC_output3_layer[0,0])))
        self.output_brake = 1.0/(1.0 + np.exp(-(self.FC_output3_layer[1,0])))  
        

     
    def publish_to_vehicle(self):
        self.pub = rospy.Publisher('/carla/hero1/vehicle_control_cmd',CarlaEgoVehicleControl,queue_size = 10)
        #use stanly control policy 
        #heading error
        yaw_diff = self.yaw_path - self.yaw  #yaw_path:ground truth heading, which means 0.0 
        crosstrack_error = 0.0-self.Lead_Veh_Position_y 
        #crosstrack error
        k_e = 0.3
        k_s = 10.0
        yaw_cross_track = np.arctan2(0.0-self.Lead_Veh_Position_y,10.0) # waypoint will be 10 m forward in y=0 
        yaw_path2ct = self.yaw_path - yaw_cross_track 
        if yaw_path2ct > 0:
            crosstrack_error = abs(crosstrack_error)
        else:
            crosstrack_error = - abs(crosstrack_error)
        yaw_diff_crosstrack = np.arctan(k_e * crosstrack_error / (k_s + self.Veh_Velocity))
        steer_expect = yaw_diff + yaw_diff_crosstrack
        
        self.control.throttle = self.output_throttle
        self.control.brake = self.output_brake
        self.control.steer = steer_expect
        self.pub.publish(self.control)
        self.rate.sleep()

    def run(self):
        global vl
        rospy.sleep(2.5)      
        if len(self.collision_list) != 0:
            r_collision = 1
        else:
            r_collision = 0
        self.collision_list.clear()           
        while not rospy.is_shutdown():
            while (self.Lead_Veh_Position_x -self.Follow_Veh_Position_x-5.0) < 100:
                for i in range(len(vl)):       
                    self.NN_INPUT[0,0] = vl[i]
                    self.NN_INPUT[1,0] = self.Veh_Velocity
                    self.NN_INPUT[2,0] = self.Veh_Accleration
                    self.from_velocity_to_gas()
                    self.publish_to_vehicle()
                    if (self.Lead_Veh_Position_x -self.Follow_Veh_Position_x) > 100 or r_collision:
                        current = rospy.get_time()
                        end = current + 2.0
                        while rospy.get_time() < end:
                            self.output_throttle = 0.0
                            self.output_brake = 1.0
                            self.publish_to_vehicle()
                        
                        break
                """
                if collision or bigger than 100 m
                """
        
def main():
    rospy.init_node('leading_test',anonymous=True)
    controller=CarlaAckermanControl()
    try:
       controller.run()
    finally:
       rospy.loginfo("bye!")

if __name__ == '__main__':
    main()
    
    
