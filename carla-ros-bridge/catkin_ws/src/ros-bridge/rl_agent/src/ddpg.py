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
from ou_noise import OUNoise
from ReplayBuffer import ReplayBuffer
from ActorNetwork import ActorNetwork
from CriticNetwork import CriticNetwork
from CarlaGame import CarlaGame
import time
from keras import backend as K
import rospy
import time
import os
import argparse

timestr = time.strftime("%Y%m%d-%H%M%S")
rospack = rospkg.RosPack()
current_path = rospack.get_path('rl_agent')




def playGame(train_indicator=0):    #1 means Train, 0 means simply Run
    BUFFER_SIZE = 2000
    BATCH_SIZE = 64
    GAMMA = 0.95
    TAU = 0.001     #Target Network HyperParameters
    LRA = 0.0003    #Learning rate for Actor
    LRC = 0.0003     #Lerning rate for Critic

    action_dim = 1  #num of action dim
    state_dim = 4  #num of features in state

    load_weight = False
    EXPLORE = 4000.0*15000
    episode_count = 4100 if (train_indicator) else 1
    max_steps = 15000 
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
    exploration_noise = OUNoise(action_dim)
    filename_epsoideReward = open(current_path + "/src/reward/" + timestr + "_EpsoideReward.txt","w")
    filename_StepAndReward = open(current_path + "/src/reward/" + timestr + "_StepAndReward.txt","w")
    
    if load_weight :#Now load the weight
        print("Now we load the weight")
        try:
            actor.model.load_weights(current_path + "/src/model/actormodel.h5")
            critic.model.load_weights(current_path + "/src/model/criticmodel.h5")
            actor.target_model.load_weights(current_path + "/src/model/actormodel.h5")
            critic.target_model.load_weights(current_path + "/src/model/criticmodel.h5")
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

        for j in range(max_steps):
            done = False   
            loss = 0 
            epsilon -= 0.1 / EXPLORE
            a_t = np.zeros([1,action_dim])
            a_t = np.clip(actor.model.predict(s_t.reshape(1, s_t.shape[0]))*1  +  exploration_noise.noise(),-1,1) #rescale            
            
            ob, r_t, done = env.step(a_t)
                       
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
        
            print("Episode", i, "Step", step, "Action", "noise", "Reward", r_t, "Loss", loss, "Epsilon", epsilon,"acceleration",a_t)
            filename_StepAndReward.write("%5.2f %5.2f %5.2f\n" %(i,step,r_t))
            step += 1
          
            if done:
                exploration_noise.reset()
                break
                
                
        if np.mod(i, 5) == 0:
            if (train_indicator):
                print("Now we save model")
                actor.model.save_weights(current_path + "/src/model/actormodel.h5", overwrite=True)
                critic.model.save_weights(current_path + "/src/model/criticmodel.h5", overwrite=True)
        
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
