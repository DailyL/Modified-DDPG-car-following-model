#!/usr/bin/env python
from collections import deque
import random
import numpy as np
import pickle
"""
class ReplayBuffer(object):

    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.num_experiences = 0
        self.buffer = deque()

    def getBatch(self, batch_size):
        # Randomly sample batch_size examples
        if self.num_experiences < batch_size:
            return random.sample(self.buffer, self.num_experiences)
        else:
            return random.sample(self.buffer, batch_size)

    def size(self):
        return self.buffer_size

    def add(self, state, action, reward, new_state, done):
        experience = (state, action, reward, new_state, done)
        if self.num_experiences < self.buffer_size:
            self.buffer.append(experience)
            self.num_experiences += 1
        else:
            self.buffer.popleft()
            self.buffer.append(experience)

    def count(self):
        # if buffer is full, return buffer size
        # otherwise, return experience counter
        return self.num_experiences

    def erase(self):
        self.buffer = deque()
        self.num_experiences = 0
        
"""

class ReplayBuffer(object):

    def __init__(self, buffer_size):
        self.buffer_size = buffer_size 
        self.num_experiences = 0      
        self.napoli_buffer = pickle.load(open('/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/clone_follower/src/buffer.pkl', 'rb'))
        self.carla_buffer = deque()
        
    def getBatch(self, batch_size):
        # Randomly sample batch_size examples
        n = batch_size/2
        
        napoli = random.sample(self.napoli_buffer, 16)
        if self.num_experiences < 16:
            carla = random.sample(self.carla_buffer, self.num_experiences)
        else:
            carla = random.sample(self.carla_buffer, 16)
            
        napoli += carla
               
        return napoli

    def size(self):
        return self.buffer_size
        
    def add(self, state, action, reward, new_state, done):
        experience = (state, action, reward, new_state, done)
        if self.num_experiences < self.buffer_size:
            self.carla_buffer.append(experience)
            self.num_experiences += 1
        else:
            self.carla_buffer.popleft()
            self.carla_buffer.append(experience)
   

    def erase(self):
        self.carla_buffer = deque()
        self.num_experiences = 0

    def count(self):
        # if buffer is full, return buffer size
        # otherwise, return experience counter
        return self.num_experiences
        
