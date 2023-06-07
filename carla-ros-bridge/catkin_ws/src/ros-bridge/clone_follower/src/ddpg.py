#!/usr/bin/env python
import numpy as np
import random
from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from tensorflow.keras.optimizers import Adam # - Works
import tensorflow.compat.v1 as tf
from tensorflow.keras import layers, models
import json

from ReplayBuffer import ReplayBuffer
from ActorNetwork import ActorNetwork
from CriticNetwork import CriticNetwork
from CarlaGame import CarlaGame
import time
from keras import backend as K
import rospy
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

data = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/datasets.npy") #load data, name"data" 1:leading 2:following 3: acceleration of following 4 : distance

def playGame(train_indicator=1):    #1 means Train, 0 means simply Run
    BUFFER_SIZE = 2000
    BATCH_SIZE = 32
    GAMMA = 0.99
    TAU = 0.001     #Target Network HyperParameters
    LRA = 0.001    #Learning rate for Actor
    LRC = 0.001     #Lerning rate for Critic

    action_dim = 2  #num of action dim
    state_dim = 4  #num of features in state
    load_weight = True
    EXPLORE = 400.0*3100
    episode_count = 401 if (train_indicator) else 1
    max_steps = 3100 
    reward = 0
    done = False
    step = 0
    epsilon = 0.05 if (train_indicator) else 0.0
    indicator = 0

    #Tensorflow GPU optimization
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    K.set_session(sess)
    actor = ActorNetwork(sess, state_dim, action_dim, BATCH_SIZE, TAU, LRA)
    critic = CriticNetwork(sess, state_dim, action_dim, BATCH_SIZE, TAU, LRC)
    buff = ReplayBuffer(BUFFER_SIZE)    #Create replay buffer
    # Generate environment
    env = CarlaGame()
    filename_epsoideReward = open("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward/"+timestr+"_EpsoideReward.txt","w")
    filename_StepAndReward = open("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/reward/"+timestr+"_StepAndReward.txt","w")
    if load_weight :#Now load the weight
        print("Now we load the weight")
        try:
            actor.model.load_weights("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/model/actormodel.h5")
            critic.model.load_weights("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/model/criticmodel.h5")
            actor.target_model.load_weights("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/model/actormodel.h5")
            critic.target_model.load_weights("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/model/criticmodel.h5")
            print("Weight load successfully")
        except:
            print("Cannot find the weight")

    for i in range(episode_count):
        print("Episode : " + str(i) + " Replay Buffer " + str(buff.count()))
        
        done = False
        ob = env.reset()
        """
        if not train_indicator:
            print ("start recording now")
        """
        s_t = np.array(ob)
     
        total_reward = 0.0
        start = 1900
        for j in range(start,start+max_steps):
            done = False   
            loss = 0 
            epsilon -= 0.05 / EXPLORE
            a_t = np.zeros([1,action_dim])
            
            a_t = actor.model.predict(s_t.reshape(1, s_t.shape[0]))*1    #rescale
            """
            if np.random.random() > epsilon:
                a_type = "Exploit"
                a_t = actor.model.predict(s_t.reshape(1, s_t.shape[0]))*1    #rescale
            else:
                a_type = "Explore"
                a_t = np.random.uniform(0.0,1.0, size=(1,2))
            """
            leader_velocity_t = data[0,j]
            follower_velocity_t = data[1,j]
            follower_accleration_t = data[2,j]
            distance_t = data[3,j]
            ob, r_t, done = env.step(a_t,follower_velocity_t,follower_accleration_t,distance_t)
                       
            s_t1 = np.array(ob)
        
            buff.add(s_t, a_t[0], r_t, s_t1, done)      #Add replay buffer
            
            #Do the batch update
            batch = buff.getBatch(BATCH_SIZE)
            states = np.asarray([e[0] for e in batch])
            actions = np.asarray([e[1] for e in batch])
            rewards = np.asarray([e[2] for e in batch])
            new_states = np.asarray([e[3] for e in batch])
            dones = np.asarray([e[4] for e in batch])
            y_t = np.asarray([e[1] for e in batch])

            target_q_values = critic.target_model.predict([new_states, actor.target_model.predict(new_states)])  
           
            for k in range(len(batch)):
                if dones[k]:
                    y_t[k] = rewards[k]
                else:
                    y_t[k] = rewards[k] + GAMMA*target_q_values[k]
       
            if (train_indicator):
                loss += critic.model.train_on_batch([states,actions], y_t) 
                a_for_grad = actor.model.predict(states)
                grads = critic.gradients(states, a_for_grad)
                actor.train(states, grads)
                actor.target_train()
                critic.target_train()

            total_reward += r_t
            s_t = s_t1
        
            print("Episode", i, "Step", step, "Action", a_type, "Reward", r_t, "Loss", loss, "Epsilon", epsilon,"Index",j, "Soll Follower Velocity",follower_velocity_t, "Soll Leader Velocity",leader_velocity_t)
            filename_StepAndReward.write("%5.2f %5.2f %5.2f\n" %(i,step,r_t))
        
            step += 1
          
            if done:
                break
                
                
        if np.mod(i, 2) == 0:
            if (train_indicator):
                print("Now we save model")
                actor.model.save_weights("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/model/actormodel.h5", overwrite=True)
                critic.model.save_weights("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/model/criticmodel.h5", overwrite=True)
        
        print("TOTAL REWARD @ " + str(i) +"-th Episode  : Reward " + str(total_reward))
        filename_epsoideReward.write("%s %s\n" % (str(i), str(total_reward)))

        print("Total Step: " + str(step))
        print("")

    env.done()
    filename_StepAndReward.close()
    filename_epsoideReward.close()
    print("Finish.")

if __name__ == "__main__":


    playGame()
