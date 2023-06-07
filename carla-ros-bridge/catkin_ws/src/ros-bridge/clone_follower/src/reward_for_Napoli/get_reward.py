import numpy as np 
from scipy.stats import norm
import math
import random
import pickle
import torch

np.set_printoptions(threshold=100000)
device = "cuda"
from collections import deque
#define parameters

a_min = -9.0 #m/s2
a_max = 5.0 #m/s2
b_comf = 2.0 #m/s2
j_comf = 2.0 #m/s2
v_des = 20.0 #m/s
T = 1.5 # s
g_min = 2.0 # m
T_lim = 15.0 # s
w_gap = 0.5
w_jerk = 0.004 
g_max = 200

compute = True

buffer = deque()



data = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/datasets.npy") #load data, name"data" 1:leading 2:following 3: acceleration of following 4 : distance

v_l = data[0]
v_f = data[1]
a_f = data[2] # action acceleration
g = data[3]




v_diff = np.zeros((len(v_l),1))
jerk = np.zeros((len(v_l),1))
rewards = np.zeros((len(v_l),1),dtype=np.float32)

dones = np.zeros((len(v_l),1),dtype=np.float32)
actions = np.zeros((len(v_l),1),dtype=np.float32)

current_a = np.zeros((len(v_l),1),dtype=np.float32) # should be the accleration of one timestep before

actions_rewards_dones = np.zeros((len(v_l),3),dtype=np.float32)
states = np.zeros((len(v_l),4),dtype=np.float32)
next_states = np.zeros((len(v_l),4),dtype=np.float32)


for i in range(len(v_l)):
    v_diff[i] = v_l[i] - v_f[i] 
    dones[i] = False
    actions[i] = a_f[i]
    current_a[i] = actions[i-1]
    current_a[0] = current_a[1]
    


for i in range(len(v_l)):
    jerk[i] = (current_a[i]-current_a[i-1])/0.1
jerk[0] = jerk[1]


if compute:
    for i in range(len(v_l)):
        if v_diff[i] < 0: 
            b_kin = (v_diff[i]**2)/g[i]
        else:
            b_kin = 0.0        
	   
        if b_kin > b_comf:
            r_safe = -np.tanh((b_kin-b_comf)/9.0)        
        else:
            r_safe = 0.0

        g_opt = v_f[i]*T + g_min
        g_var = 0.5*g_opt
        g_lim = v_f[i]*T_lim + 2*g_min
        g_star = g_opt -0.5  

        if g[i] < g_star:
            r_gap = norm(0,1).pdf((g[i] - g_opt)/g_var)/norm(0,1).pdf(0)        
        else:
            r_gap = (norm(0,1).pdf((g[i] - g_opt)/g_var)/norm(0,1).pdf(0))*(1 - (g[i]-g_star)/(g_lim-g_star))

        r_jerk = (jerk[i]**2)/4
        rewards[i] = r_safe + w_gap*r_gap + w_jerk*r_jerk

        states[i,0] = v_f[i]/v_des
        states[i,1] = g[i]/g_max 
        states[i,2] = v_diff[i]/v_des
        states[i,3] = (a_f[i] - a_min)/(a_max - a_min)

        actions_rewards_dones[i,0] = actions[i]
        actions_rewards_dones[i,1] = rewards[i]
        actions_rewards_dones[i,2] = dones[i]
        actions[i] = actions[i]/9.0
new_states = np.zeros((33036, 4),dtype=np.float32)



for i in range(len(states)-1):
    new_states[i] = states[i+1]


np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/actions.npy",actions)
np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/rewards.npy",rewards)
np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/dones.npy",dones)

#     np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/actions_rewards_dones.npy",actions_rewards_dones)
np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/states.npy",states)
np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/new_states.npy",(new_states))

# get_data = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/actions_rewards_dones.npy")
# get_states = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/states.npy")
# actions = get_data[:,0]/9.0
# rewards = get_data[:,1]
# dones = get_data[:,2]



# new_states = np.zeros((33036, 4),dtype=np.float32)



# for i in range(len(get_states)-1):
#     new_states[i] = get_states[i+1]
    

# for i in range(len(dones)):
#     if np.mod(i, 500) == 0:
#         dones[i] = True


# for i in range(len(actions)): 
#     experience = (torch.tensor(get_states[i]).to(device), torch.tensor(actions[i]).to(device), torch.tensor(rewards[i]).to(device), torch.tensor(new_states[i]).to(device), torch.tensor(dones[i]).to(device))
#     buffer.append(experience)
  
# buffer_np = []
# pickle.dump(buffer, open('buffer.pkl', 'wb'))
# buffer_np.append(get_states)
# buffer_np.append(actions)
# buffer_np.append(rewards)
# buffer_np.append(new_states)
# buffer_np.append(dones)        

# # np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/buffer.npy",buffer)
# np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/actions.npy",(actions))
# np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/rewards.npy",(rewards))
# np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/new_states.npy",(new_states))
# np.save("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/dones.npy",(dones))



# actions = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/actions.npy",allow_pickle=True)
# dones2 = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/dones.npy",allow_pickle=True)
# print(actions.shape)
# buffer = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward_for_Napoli/buffer.npy",allow_pickle=True)
# ind = np.random.randint(low = 0, high = 100, size = 5)

# print(buffer[0])

# my_buffer_2 = pickle.load(open('buffer.pkl', 'rb'))


# ind = np.random.randint(low = 0, high = 100, size = 5)



# sample_buffer = random.sample(my_buffer_2, 32)

# sample_buffer = random.sample(my_buffer_2, 32)
# print(sample_buffer)






