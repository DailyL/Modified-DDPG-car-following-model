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
from pub_to_leading import CarlaPublisher
from random import randrange
from random import randint, choice

timestr = time.strftime("%Y%m%d-%H%M%S")

data = np.load("/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/datasets.npy") #load data, name"data" 1:leading 2:following 3: acceleration of following 4 : distance

def playGame(train_indicator=1):    #1 means Train, 0 means simply Run
    BUFFER_SIZE = 4000
    BATCH_SIZE = 32
    GAMMA = 0.99
    TAU = 0.001     #Target Network HyperParameters
    LRA = 0.001    #Learning rate for Actor
    LRC = 0.001     #Lerning rate for Critic

    action_dim = 2  #num of action dim
    state_dim = 4  #num of features in state
    load_weight = True
    EXPLORE = 4000.0*2000
    episode_count = 4001 if (train_indicator) else 1
    max_steps = 2000 
    reward = 0
    done = False
    step = 0
    epsilon = 0.1 if (train_indicator) else 0.0
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
        for _ in range(1):
            r = choice([(1,2),(1890,1891),(1303,1429),(700,701),(1474,1519),(1964,2011),(2273,2806),(3151,3161),(4282,4283),(4960,5022),(5670,5887),(7582,7607),(7864,7976),(8036,8350),(8826,8883),(9276,9340),(9799,9841),(10039,10090),(11714,11720),(12323,12455),(12503,12542),(12940,13043),(13267,13843),(14157,14180),(15989,16041),(16696,16950),(18596,18627),(18876,19000),(19086,19370),(19834,19906),(20269,20380),(20825,20860),(21077,21106),(23344,23476),(23969,24064),(24296,24857),(27023,27079),(27731,27922),(29888,30033),(30091,30391),(30849,30923)])
#(31297,31398),(31845,31885),(32092,32140)
        rangdom_index = randint(*r)
        
        for j in range(max_steps):
            done = False   
            loss = 0 
            epsilon -= 0.1 / EXPLORE
            a_t = np.zeros([1,action_dim])
            
            if np.random.random() > epsilon:
                a_type = "Exploit"
                a_t = actor.model.predict(s_t.reshape(1, s_t.shape[0]))*1    #rescale
            else:
                a_type = "Explore"
                a_t = np.random.uniform(0.0,1.0, size=(1,2))
            
             
            follower_velocity_t = data[1,rangdom_index]
            follower_accleration_t = data[2,rangdom_index]
            
            distance_t = data[3,j]
            ob, r_t, done = env.step(a_t,follower_velocity_t,follower_accleration_t,distance_t)
            pub = CarlaPublisher(rangdom_index,max_steps,done)
            pub.run()
            rangdom_index = rangdom_index + 1           
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
        
            print("Episode", i, "Step", step, "Action", a_type, "Reward", r_t, "Loss", loss, "Epsilon", epsilon, "Index",rangdom_index, "Soll Follower Velocity",follower_velocity_t)
            filename_StepAndReward.write("%5.2f %5.2f %5.2f\n" %(i,step,r_t))
            step += 1
            if done:
                break
                
                
        if np.mod(i, 5) == 0:
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
