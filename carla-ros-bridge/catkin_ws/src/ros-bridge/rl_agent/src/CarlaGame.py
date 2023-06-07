#!/usr/bin/env python
import sys
import rospy
import numpy as np
from geometry_msgs.msg import Pose, PoseStamped
from sensor_msgs.msg import JointState, Image
from std_msgs.msg import Header
from tf import TransformListener
import math
from nav_msgs.msg import Odometry
from carla_msgs.msg import CarlaEgoVehicleStatus  
from carla_msgs.msg import CarlaEgoVehicleControl  
from carla_msgs.msg import CarlaEgoVehicleInfo  
from carla_ackermann_msgs.msg import EgoVehicleControlInfo 
from carla_msgs.msg import CarlaCollisionEvent  
from scipy.stats import norm


class CarlaGame():
    def __init__(self):
        #init code
        rospy.init_node("CarlaGame")
        self.currentDist = 1
        self.previousDist = 1
        self.reached = 0
        self.Lead_control = CarlaEgoVehicleControl()
        self.Follow_control = CarlaEgoVehicleControl()
        self.Lead_Veh_Velocity = 0.0
        self.Lead_Veh_Accleration = 0.0
        self.Lead_Veh_Position_x = 0.0
        self.Lead_Veh_Position_y = 0.0
        self.Follow_Veh_Accleration = 0.0
        self.Follow_Veh_Accleration_past = 0.0
        self.Follow_Veh_Velocity = 0.0
        self.Follow_Veh_Position_x = 0.0
        self.Follow_Veh_Position_y = 0.0
        self.hero2_acceleration = 0.0
        self.current_time = 0.0
        self.t_diff = 0.0
        self.Previous_time = 0.0
        self.previous_velocity = 0.0
        self.NN_INPUT = np.matrix([[0.0],[0.0],[0.0]])
        self.output_throttle = 0.0
        self.output_brake =  0.0
        self.speed = 0.0
        # intial value of Q function from pre-trained NN
        self.action_size = 1

        self.v_des = 20.0 #19.43276126    #m/s
        self.a_min = -9.0 #-5.51127117000001       #m2/s
        self.a_max = 5.0 #4.72755725        #m2/s
        self.s_max = 200.0 #31.79662929      #m
        self.collision_other_actor_id = 0
        self.collision_list=[]
        self.yaw_path = 0.0

        self.states_free_driving = np.zeros((2,1))
        self.states_car_following = np.zeros((4,1))



        self.rate = rospy.Rate(10)
        
        
        
        #SMALL CONTROL NETWORK
        
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
        
        self.sub_leading_vehicle_position = rospy.Subscriber("/carla/hero1/odometry",Odometry,self.leading_vehicle_position_callback,queue_size = 10)
        self.sub_leading_vehicle_velocity = rospy.Subscriber("/carla/hero1/vehicle_status",CarlaEgoVehicleStatus,self.leading_vehicle_velocity_callback,queue_size = 10)
        self.sub_following_vehicle_acceleration_and_velocity = rospy.Subscriber("/carla/hero2/vehicle_status",CarlaEgoVehicleStatus,self.following_vehicle_acceleration_and_velocity_callback,queue_size = 10)
        
        self.sub_leading_vehicle_position = rospy.Subscriber("/carla/hero2/odometry",Odometry,self.following_vehicle_position_callback,queue_size = 10)
        self.sub_collision = rospy.Subscriber("/carla/hero2/collision", CarlaCollisionEvent, self.following_vehicle_collision_callback,queue_size = 10)
        self.pub = rospy.Publisher('/carla/hero2/vehicle_control_cmd',CarlaEgoVehicleControl,queue_size = 10)
        self.reset()
        
    def from_velocity_to_gas(self):
        self.FC_output1_layer = np.maximum((np.dot(self.FC_w1,self.NN_INPUT) + self.FC_b1),0.0)
        self.FC_output2_layer = np.maximum((np.dot(self.FC_w2,self.FC_output1_layer) + self.FC_b2),0.0)
        self.FC_output3_layer =np.dot(self.FC_w3,self.FC_output2_layer)+self.FC_b3
        
        self.output_throttle = 1.0/(1.0 + np.exp(-(self.FC_output3_layer[0,0])))
        self.output_brake = 1.0/(1.0 + np.exp(-(self.FC_output3_layer[1,0])))
        return self.output_throttle, self.output_brake
                
    def leading_vehicle_position_callback(self,data):
         self.Lead_Veh_Position_x = data.pose.pose.position.x
         self.Lead_Veh_Position_y = data.pose.pose.position.y

    def leading_vehicle_velocity_callback(self,data):
        self.Lead_Veh_Velocity = data.velocity
 
    def following_vehicle_acceleration_and_velocity_callback(self,data):
        self.Follow_Veh_Velocity = data.velocity
        self.Follow_Veh_Accleration = data.acceleration.linear.x
        self.Follow_Veh_Accleration_past = self.Follow_Veh_Accleration
        self.yaw = data.orientation.y
               
    def following_vehicle_position_callback(self,data):      
        self.Follow_Veh_Position_y = data.pose.pose.position.y
        self.Follow_Veh_Position_x = data.pose.pose.position.x
    
    def following_vehicle_collision_callback(self, data):
        self.collision_other_actor_id = data.other_actor_id
        self.collision_list.append(self.collision_other_actor_id)
                    	           

    def reset(self):  
    
    #reseat function to reset simulation
    #return the initial states after reset
    #return: states               
        self.lead_pub = rospy.Publisher('/carla/hero1/vehicle_control_cmd',CarlaEgoVehicleControl,queue_size = 10)
        self.follow_pub = rospy.Publisher('/carla/hero2/vehicle_control_cmd',CarlaEgoVehicleControl,queue_size = 10)
        self.Follow_control = CarlaEgoVehicleControl()        
        self.Lead_control = CarlaEgoVehicleControl()        
        self.Lead_control.throttle = 0.0
        self.Lead_control.brake = 1.0
        
        
        self.Follow_control.throttle = 0.0
        self.Follow_control.brake = 1.0
        
        self.lead_pub.publish(self.Lead_control)
        self.follow_pub.publish(self.Follow_control)

        self.pub.publish(self.Lead_control)        
        self.pub.publish(self.Follow_control)        
        

        #get initial states
        self.reached = 0
        status1 = self.Follow_Veh_Velocity/self.v_des
        status2 = self.getRelativPosition()/self.s_max 
        status3 = self.getRelativSpeed()/self.v_des
        status4 = (self.Follow_Veh_Accleration - self.a_min)/(self.a_max - self.a_min)
        
        state = [status1,status2,status3,status4]
        return state
        
    def getRelativSpeed(self):        
    	lead_speed = self.Lead_Veh_Velocity        
    	follow_speed = self.Follow_Veh_Velocity 
    	relative_speed = lead_speed - follow_speed   
    	
    	return relative_speed
    	
    	
    def getRelativPosition(self):        
    	lead_position = self.Lead_Veh_Position_x        
    	follow_position = self.Follow_Veh_Position_x 
    	s = lead_position - follow_position  -5.0
    	if s > self.s_max:
            s = self.s_max
    	return s
	 
                           
    def setReward(self):
    

        #new reward
        b_comf = 2.0	
        T = 1.5
        T_lim = 15.0
        g_min = 2.0
        velocity_diff = self.getRelativSpeed()
        gap = self.getRelativPosition()
        w_gap = 0.5
        w_jerk = 0.004
        if velocity_diff < 0: 
            b_kin = (velocity_diff**2)/gap
        else:
            b_kin = 0.0        
                   
        if b_kin > b_comf:
            r_safe = -np.tanh((b_kin-b_comf)/9.0)        
        else:
            r_safe = 0.0
            
        g_opt = self.Follow_Veh_Velocity*T + g_min
        
        g_var = 0.5*g_opt
        
        g_lim = self.Follow_Veh_Velocity*T_lim + 2*g_min

        g_star = g_opt -0.5  
              
        if gap < g_star:
            r_gap = norm(0,1).pdf((gap - g_opt)/g_var)/norm(0,1).pdf(0)        
        else:
            r_gap = (norm(0,1).pdf((gap - g_opt)/g_var)/norm(0,1).pdf(0))*(1 - (gap-g_star)/(g_lim-g_star))
            
        jerk = (self.Follow_Veh_Accleration - self.Follow_Veh_Accleration_past)/0.1
        r_jerk = (jerk**2)/4
            
                    
                    
        reward = r_safe + w_gap*r_gap + w_jerk*r_jerk        



        print  (reward)
        return reward

    def step(self,action):

    #step function
    #take an action and return updated states
    #return: state, reward, done
        done = False
        
        #use stanly control policy 
        #heading error
        yaw_diff = self.yaw_path - self.yaw  #yaw_path:ground truth heading, which means y=0 
        crosstrack_error = 0.0-self.Follow_Veh_Position_y
        #crosstrack error
        k_e = 0.3
        k_s = 10.0
        yaw_cross_track = np.arctan2(0.0-self.Follow_Veh_Position_y,10.0) # waypoint will be 10 m forward in y=0 
        yaw_path2ct = self.yaw_path - yaw_cross_track 
        if yaw_path2ct > 0:
            crosstrack_error = abs(crosstrack_error)
        else:
            crosstrack_error = - abs(crosstrack_error)
        yaw_diff_crosstrack = np.arctan(k_e * crosstrack_error / (k_s + self.Follow_Veh_Velocity))
        steer_expect = yaw_diff + yaw_diff_crosstrack
        
        accleration = min(action[0,0]*9.0,5.0)
        
        self.NN_INPUT[0,0] = self.Follow_Veh_Velocity + accleration*0.1
        self.NN_INPUT[1,0] = self.Follow_Veh_Velocity
        self.NN_INPUT[2,0] = self.Follow_Veh_Accleration
        
        throttle_t, brake_t = self.from_velocity_to_gas()
        
        
        self.Follow_control = CarlaEgoVehicleControl()
        if accleration > 4.0 and self.Follow_Veh_Velocity < 0.2 :
            self.Follow_control.throttle = 1.0
            self.Follow_control.brake = 0.0
        elif accleration == -9.0:
            self.Follow_control.throttle = 0.0
            self.Follow_control.brake = 1.0    
        else:
            self.Follow_control.throttle = throttle_t
            self.Follow_control.brake = brake_t
        self.Follow_control.steer = steer_expect
        self.pub.publish(self.Follow_control)        
        self.rate.sleep()
             
        
        status1 = self.Follow_Veh_Velocity/self.v_des
        status2 = self.getRelativPosition()/self.s_max 
        status3 = self.getRelativSpeed()/self.v_des
        status4 = (self.Follow_Veh_Accleration - self.a_min)/(self.a_max - self.a_min)
        
        state = [status1,status2,status3,status4]
        reward = self.setReward()
        
        if len(self.collision_list) != 0 or (self.Lead_Veh_Position_x -self.Follow_Veh_Position_x)  <= 0:
            done = True
        else:
            done = False

           
        self.collision_list.clear()        
        return state, reward, done
    def done(self):
        rospy.signal_shutdown("done")               
if __name__ == "__main__":
            r = CarlaGame()
            print (r.setReward())
            r.reset()
            print (r.setReward())





