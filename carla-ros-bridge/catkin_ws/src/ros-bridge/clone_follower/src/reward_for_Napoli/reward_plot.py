import numpy as np 
from scipy.stats import norm
import math
import random
import pickle
np.set_printoptions(threshold=100000)
from collections import deque
import matplotlib.pyplot as plt




data = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/datasets.npy") #load data, name"data" 1:leading 2:following 3: acceleration of following 4 : distance

v_l = data[0]
v_f = data[1]
a_f = data[2] # action acceleration
g = data[3]
time = np.arange(0, len(v_l)/10, 0.1)

get_data = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/actions_rewards_dones.npy")


actions = get_data[:,0]/9.0
rewards = get_data[:,1]
dones = get_data[:,2]


plt.figure(1)

fig,ax1 = plt.subplots()
ax1.plot(time,g,color='g')

ax2=ax1.twinx()
ax2.plot(time,rewards,color='r')
plt.show()



