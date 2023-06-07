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
from ackermann_msgs.msg import AckermannDrive  # pylint: disable=import-error
from carla_msgs.msg import CarlaEgoVehicleStatus  # pylint: disable=no-name-in-module,import-error
from carla_msgs.msg import CarlaEgoVehicleControl  # pylint: disable=no-name-in-module,import-error
from carla_msgs.msg import CarlaEgoVehicleInfo  # pylint: disable=no-name-in-module,import-error
from carla_ackermann_msgs.msg import EgoVehicleControlInfo  # pylint: disable=no-name-in-module,import-error
from carla_msgs.msg import CarlaCollisionEvent  
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
import csv

from carla_ackermann_control import carla_control_physics as phys

from simple_pid import PID

#data = np.loadtxt("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/rl_agent/src/full_napoli_datasets.csv")
#vl = data[0,:].reshape(33036,1)



class CarlaPublisher(object):
    def __init__(self,index,max_steps,done):
        self.control = CarlaEgoVehicleControl()
        self.ackermann_cmd = AckermannDrive()
        self.rate = rospy.Rate(10)
        self.data = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/datasets.npy")
        self.vl = self.data[0]
        self.a = self.data[4]
        self.NN_INPUT = np.matrix([[0.0],[0.0],[0.0]])
        self.output_throttle = 0.0
        self.output_brake =  0.0
        self.Veh_Velocity = 0.0
        self.Veh_Accleration = 0.0
        self.follower_control_gas = 0.0
        
        
        """
        self.FC_w1 = np.array([[-0.4535,  0.6297,  0.0591],
        [ 0.1756, -0.1164,  0.7714],
        [ 0.1634, -0.1469, -0.2020],
        [ 0.8457, -0.8748, -0.0331],
        [-0.3602,  0.2329,  0.0144],
        [ 0.4584, -0.5377, -1.3627],
        [-0.2590,  0.2129, -0.1822],
        [ 0.4910, -0.8561,  0.5401]])

        self.FC_w2 = np.array([[ 3.1454e-01, -1.1654e+00,  7.1887e-02,  3.5039e-01,  7.6030e-02,
          7.6008e-01,  3.9665e-01, -2.6701e+00],
        [-4.2820e-01,  2.6656e-01,  3.1396e-02,  1.9740e+00, -3.3000e-02,
          1.6408e-01,  3.6656e-02, -5.0578e-01],
        [ 2.3929e-01, -2.5825e-01, -1.5738e-01,  1.9140e+00, -5.8518e-01,
         -8.8950e-01, -4.0643e-01,  5.4190e-01],
        [ 1.5191e-01, -2.6728e-01, -3.8524e-01, -5.7440e-02, -3.1482e-01,
          6.4942e-02, -2.5156e-01,  3.3663e-01],
        [ 2.4823e-01,  1.1051e+00,  2.4577e-02,  3.7483e-01, -5.2793e-02,
         -7.6233e-01, -1.5573e-01,  1.0048e+00],
        [-1.0306e-01,  9.2717e-01,  3.7107e-01,  6.9146e-01, -5.3043e-01,
          1.2366e+00,  4.8283e-01, -9.0362e-01],
        [ 1.5347e-01, -2.6597e-01, -2.2952e-01, -1.0870e+00,  1.2412e+00,
         -5.8692e-01,  3.8997e-01, -5.0641e-01],
        [-6.2465e-01, -1.6345e-03, -4.7451e-01, -1.8029e+00,  3.5458e-01,
         -4.5042e+00,  6.3823e-01,  4.2301e-01],
        [-4.6072e+00, -1.5957e-01, -1.3282e+00,  2.2196e-01, -1.0131e-01,
          1.3026e+00, -3.4687e-01, -1.8276e+00],
        [ 7.2327e-01,  5.3809e-01,  4.6369e-01, -1.4408e+00,  6.5706e-01,
         -8.4090e-01,  1.4680e-02, -4.9688e-01],
        [-3.0985e-01,  4.2427e-01, -7.2964e-03,  1.4226e+00, -8.1731e-02,
          5.6099e-02,  1.8268e-01, -7.4154e-01],
        [ 8.4502e-01, -4.0879e-01,  3.9771e-01,  2.1411e-01, -2.4513e-01,
         -6.9500e-01,  4.8316e-01,  2.4184e-01],
        [ 9.5589e-03, -1.7254e-01, -2.6746e-01, -1.0303e-01, -2.0547e-02,
          1.4358e-01, -2.1177e-01,  1.9658e-01],
        [-3.4566e-02, -1.6827e-01, -1.3353e-03, -2.6191e-01, -4.5171e-02,
         -1.0206e-01, -2.5087e-01,  1.8963e-01],
        [-6.0624e-01, -1.6171e-02, -8.0672e-02,  1.6903e+00,  4.3319e-01,
         -6.0464e-01, -5.7976e-01, -6.6505e-02],
        [ 1.5076e-01, -2.7098e-02,  1.0381e-01,  1.7080e+00, -6.5262e-01,
         -2.0239e-01, -1.0251e-01,  6.2313e-02]])
	
        self.FC_w3 = np.array([[-5.3833e-02, -4.5547e-01, -1.6122e-01, -1.3313e-02,  3.5905e-02,
         -8.6591e-02, -1.5276e-01, -3.2212e-01,  1.1569e-01, -4.4521e-02,
         -2.1116e-01, -1.9325e-01, -2.1975e-01,  1.5801e-02, -2.9992e-01,
         -2.5995e-01],
        [ 1.0473e-01, -1.4858e-01,  2.0392e-01, -4.8946e-03,  7.9559e-03,
         -1.7919e-02, -7.5932e-02, -8.6121e-02, -1.7935e-01, -1.3332e-01,
         -1.8325e-01, -2.6507e-01, -2.2567e-01, -2.3394e-01, -2.7682e-01,
         -4.8429e-02],
        [-6.1437e-01,  2.1275e+00,  1.2211e+00, -6.1400e-03,  1.8240e-01,
          3.9201e-01, -1.1427e+00, -1.2101e+00, -9.0058e-01, -6.3356e-01,
          7.9849e-01,  5.6277e-01, -1.5579e-02, -1.8207e-01,  6.4260e-01,
          1.2135e+00],
        [-9.9096e-01, -1.5329e+00, -9.1299e-01, -8.0172e-02,  7.1385e-01,
         -4.3181e-01,  2.0249e+00,  1.0988e+00,  1.0976e-01,  5.4252e-01,
         -2.1792e-01,  2.6687e-01,  1.6386e-01,  1.6386e-01, -9.0777e-01,
         -1.5417e+00],
        [ 4.1544e-01,  1.9738e+00,  9.9477e-01, -2.4731e-01, -2.8158e-02,
         -1.2064e-01, -1.1844e+00,  2.6956e-01, -1.6525e+00, -5.0535e-01,
          9.1980e-01, -1.4924e-01, -1.5317e-01,  5.1190e-02, -5.9198e-01,
          1.4089e+00],
        [ 4.0403e-02,  8.8105e-01,  3.9968e-01,  3.7563e-03, -3.4303e-01,
         -2.3848e-01,  3.3211e-01,  5.0384e-02, -1.5726e-01, -4.7196e-01,
          6.2378e-01, -5.7119e-01, -5.1229e-02,  1.0520e-01,  6.6045e-01,
         -3.5955e-01],
        [ 3.9982e-01, -1.4631e+00, -9.5625e-02, -2.3619e-02, -3.2691e+00,
          2.9249e-01,  2.2764e-01, -3.4348e-01,  8.0445e-01,  1.5381e+00,
         -7.4405e-01, -8.2661e-01,  3.1607e-02, -2.0475e-01,  4.7989e-01,
         -3.8355e-01],
        [ 1.7046e-01, -9.2538e-01, -7.0679e-01, -1.5510e-01,  4.8308e-01,
         -5.4218e-01, -1.9559e+00,  9.9394e-01,  1.9407e-02, -1.6029e-01,
         -1.0944e+00, -7.9429e-01, -1.9981e-01,  2.3065e-01, -4.3787e+00,
         -1.7462e+00]])
         
        self.FC_w4 =  [[-0.3280, -0.0116,  3.2447, -3.3848,  0.9921, -0.8117, -1.8796, -1.5023],
        [-0.0710, -0.1465, -1.0997,  0.4577, -4.5542, -0.2528, -0.6988, -2.6845]]
        """
        """
        self.FC_w1 = np.array([[ 2.2718e-04,  4.2190e-01,  1.0131e+00],
        [-9.6073e-02,  5.9143e-02, -1.7820e-01],
        [ 3.6326e-01, -4.3053e-01, -3.2264e-01],
        [ 1.4146e-01,  3.7359e-01, -2.4664e-01],
        [ 1.3339e-01,  2.0966e-01, -5.5970e-01],
        [-7.1991e+00, -7.7831e+00, -1.9976e+00],
        [ 7.5894e-02, -1.0255e-01, -3.2438e-01],
        [-2.7152e-01,  2.2212e-01,  1.1978e+00]])

        self.FC_w2 = np.array([[-0.5154,  1.4728, -0.3294,  0.1902, -0.0591, -0.2668,  0.1737,  0.1475],
        [-0.2410, -0.2574,  0.2556, -0.0532, -0.1142,  0.1990, -0.0600,  0.1456],
        [-0.2211,  0.8657, -0.3527,  0.3370,  0.1340, -0.0809, -0.4713, -0.0807],
        [ 0.0340, -0.0169,  0.3444,  0.5803,  0.3704,  0.4765, -0.1706, -0.1591],
        [-0.7130,  0.2219,  0.1948, -0.5089, -0.6456,  1.4235,  0.0764, -0.4362],
        [ 0.3349, -0.5621, -0.1930, -0.2051,  0.3030, -0.1704, -1.3764,  0.1007],
        [-0.2208,  0.0538, -0.0770,  0.0061, -0.1446,  1.6357, -0.3239, -0.1387],
        [-0.2352,  0.5681,  0.1226,  0.0033,  0.2210,  1.1984,  0.2556, -0.1643],
        [-0.3274,  0.7519,  0.0197, -0.3615, -0.0122,  1.8889,  0.4617,  0.6072],
        [-0.0409,  0.0833, -0.0626, -0.2059, -0.2820,  0.0494,  0.1767, -0.3054],
        [ 0.0757,  0.5134, -0.2335,  0.0272,  0.1458, -0.4260,  0.4862,  0.3939],
        [-0.3515,  1.3791,  0.3520,  0.1787, -0.1343,  0.3499,  0.8017, -0.4712],
        [-0.2846,  0.9283,  0.0472,  0.0744,  0.1106,  0.3532, -0.1173,  0.3842],
        [-0.1929, -0.3193, -0.0930, -0.2789, -0.3525,  0.0335,  0.0046, -0.1290],
        [-0.3873,  0.0658, -0.2810,  0.4267,  0.2392, -0.1583,  0.1293, -1.1871],
        [ 0.0158, -0.4046, -0.2719,  0.2862,  0.3479, -0.4699,  0.1279,  0.0451]])
	
        self.FC_w3 = np.array([[ 0.1844, -0.1004, -0.3507,  0.0673, -0.3456, -0.6531, -0.1984,  0.2931,
         -0.2583,  0.1259,  0.3503, -0.0448,  0.1037, -0.2245,  0.4338,  0.2213],
        [-0.1308,  0.0398,  0.3067,  0.3060,  0.4498,  0.3875,  1.1983,  0.6548,
          0.2080, -0.2468,  0.1650,  0.3072,  0.1001, -0.2173, -0.6608,  0.2942],
        [-0.2479, -0.1011, -0.1686, -0.1296,  0.1062, -0.1668,  0.0290,  0.1216,
         -0.1382, -0.1878, -0.0673,  0.1005, -0.0202, -0.0280,  0.2204,  0.1282],
        [ 0.2244,  0.2882,  0.2408, -0.0756, -0.6412, -1.3537, -0.7023, -0.2488,
          0.2484, -0.0219,  0.1759, -0.1531,  0.4248,  0.0115,  0.6002,  0.1182],
        [-0.0738, -0.2277,  0.2355,  0.2335,  0.9274,  1.0419,  0.9352,  0.2113,
          0.7939, -0.0024,  0.0885, -0.0079,  0.0564,  0.0929, -0.8007,  0.2946],
        [ 0.1992,  0.1623,  0.3127, -0.2499, -0.8519, -1.1043, -0.2960,  0.0420,
          0.2006,  0.1082,  0.3498,  0.0399,  0.0537,  0.1996,  0.9249, -0.0464],
        [-1.2642, -0.0945, -0.1022,  0.3540,  0.2580, -0.3924, -0.0040, -1.1178,
          0.5781,  0.0490,  0.1444, -1.6886, -0.1851, -0.2482, -1.8530,  0.3468],
        [-0.0204,  0.1902,  0.0145,  0.1149, -0.0702, -0.2613,  0.0908, -0.2593,
          0.1086, -0.0073, -0.0104, -0.2725, -0.1634, -0.1500, -0.1531, -0.2123]])
         
        self.FC_w4 =  np.array([[ 0.1553, -0.4258,  0.1067,  0.3139, -0.5237,  0.3463,  1.1879, -0.2115],
        [-0.7641, -0.2433, -0.0583, -0.3635,  0.3633, -0.4367,  0.0038,  0.2161]])
        
        
        
        
        
        
        
         
         
         
 
        self.FC_b1 = np.array([-0.9603,  1.8613, -0.2003,  0.7577,  0.4361,  0.8080,  1.7726,  0.4289]).reshape(8,1)


        self.FC_b2 = np.array([ 1.1035, -0.0999,  0.5227,  0.2047,  0.1527, -1.3034,  0.0925,  1.0095,
         1.1524, -0.2799,  0.7448,  1.0873,  0.0086, -0.1539, -0.1177,  0.1618]).reshape(16,1)
        self.FC_b3 = np.array([ 0.8871,  0.1359, -0.1050,  0.2328, -0.0892,  0.6220, -0.0245, -0.2675]).reshape(8,1)
        self.FC_b4 = np.array([ 0.2442, -0.3314]).reshape(2,1)
        """

#2 hidden layers

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







        
        self.sub_vehicle_velocity = rospy.Subscriber("/carla/hero3/vehicle_status",CarlaEgoVehicleStatus,self.leading_velocity_callback,queue_size = 1)
        self.sub_leading_vehicle_position = rospy.Subscriber("/carla/hero3/odometry",Odometry,self.leading_vehicle_position_callback,queue_size = 1)
        
        self.sub_leading_vehicle_position = rospy.Subscriber("/carla/hero4/odometry",Odometry,self.following_vehicle_position_callback,queue_size = 1)
        self.sub_collision = rospy.Subscriber("/carla/hero4/collision", CarlaCollisionEvent, self.following_vehicle_collision_callback,queue_size = 1)
        self.sub_follower_control = rospy.Subscriber('/carla/hero4/vehicle_control_cmd',CarlaEgoVehicleControl,self.follower_control_callback,queue_size = 1)
        self.collision_other_actor_id = 0
        self.collision_list=[]
        self.start_index = index
        self.max_steps = max_steps
        self.Lead_Veh_Position_x = 0.0
        self.Follow_Veh_Position_x = 0.0
        self.done = done
    def follower_control_callback(self,data):
    
         self.follower_control_gas = data.throttle    
    
    
    
    
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
        
        
        
    def position_difference(self):
        position_difference = self.Lead_Veh_Position_x - self.Follow_Veh_Position_x - 5.0
        
        return position_difference
        
    def from_velocity_to_gas(self):
        #2hidden layers control
            
        self.FC_output1_layer = np.maximum((np.dot(self.FC_w1,self.NN_INPUT) + self.FC_b1),0.0)
        self.FC_output2_layer = np.maximum((np.dot(self.FC_w2,self.FC_output1_layer) + self.FC_b2),0.0)
        self.FC_output3_layer =np.dot(self.FC_w3,self.FC_output2_layer)+self.FC_b3
        
        self.output_throttle = 1.0/(1.0 + math.exp(-(self.FC_output3_layer[0,0])))
        self.output_brake = 1.0/(1.0 + math.exp(-(self.FC_output3_layer[1,0])))    
    
        #3hidden layers control
        """
        self.FC_output1_layer = np.maximum((np.dot(self.FC_w1,self.NN_INPUT) + self.FC_b1),0.0)
        self.FC_output2_layer = np.maximum((np.dot(self.FC_w2,self.FC_output1_layer) + self.FC_b2),0.0)
        self.FC_output3_layer = np.maximum((np.dot(self.FC_w3,self.FC_output2_layer) + self.FC_b3),0.0)
        self.FC_output4_layer =np.dot(self.FC_w4,self.FC_output3_layer)+self.FC_b4
        
        self.output_throttle = 1.0/(1.0 + math.exp(-(self.FC_output4_layer[0,0])))
        self.output_brake = 1.0/(1.0 + math.exp(-(self.FC_output4_layer[1,0])))  
        """

     
    def publish_to_vehicle(self):
        
        
        self.pub = rospy.Publisher('/carla/hero3/vehicle_control_cmd',CarlaEgoVehicleControl,queue_size = 1)
        self.control.throttle = self.output_throttle
        self.control.brake = self.output_brake
        self.pub.publish(self.control)
        self.rate.sleep()
        
        """
        self.pub = rospy.Publisher('/carla/hero3/ackermann_cmd',AckermannDrive,queue_size = 10)
        self.ackermann_cmd.steering_angle = 0.0
        self.ackermann_cmd.steering_angle_velocity = 0.0
        self.ackermann_cmd.acceleration = 0.0
        self.ackermann_cmd.speed = velocity
        self.pub.publish(self.ackermann_cmd)
        self.rate.sleep()
        """
    def run(self):
        if len(self.collision_list) != 0:
            r_collision = 1
        else:
            r_collision = 0
        self.collision_list.clear()
        print("soll leader velocity",self.vl[self.start_index]) 
        
        if (self.Lead_Veh_Position_x -self.Follow_Veh_Position_x)  <= 30:
            #NN control      
            self.NN_INPUT[0,0] = self.vl[self.start_index]
            self.NN_INPUT[1,0] = self.Veh_Velocity
            self.NN_INPUT[2,0] = self.Veh_Accleration
            self.from_velocity_to_gas()
            self.publish_to_vehicle()
            print("publish one action")
            #pid control
            """
            self.publish_to_vehicle(self.vl[self.start_index])
            """
        elif (self.Lead_Veh_Position_x -self.Follow_Veh_Position_x) > 30:
            self.pub2 = rospy.Publisher('/carla/hero3/vehicle_control_cmd',CarlaEgoVehicleControl,queue_size = 1)
            self.control.throttle = 0.0
            self.control.brake = 1.0
            self.pub2.publish(self.control)
            self.rate.sleep()
        
       
        

                
    
    
