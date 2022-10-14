#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from pomegranate import *
import numpy as np


# In[7]:


X = numpy.random.randint(2, size=(100, 6))
model = MarkovNetwork.from_samples(X)


# In[14]:


wall_dist = DiscreteDistribution({'L': 1./10, 'M': 9./10})
robot_move = ConditionalProbabilityTable(
        [['L', 'W', 0.1],
         ['L', 'S', 0.9],
         ['M', 'W', 0.8],
         ['M', 'S', 0.2]], [wall_dist])

passed_door = ConditionalProbabilityTable(
        [['W', 'T', 0.0],
         ['W', 'F', 0.95],
         ['S', 'T', 0.9],
         ['S', 'F', 0.1]], [robot_move])

s1 = Node(wall_dist, name="wall distance")
s2 = Node(robot_move, name="robot moves")
s3 = Node(passed_door, name="door passed")

model = BayesianNetwork("Robot Door Walk Problem")
model.add_states(s1, s2, s3)
model.add_edge(s1, s2)
model.add_edge(s2, s3)
model.bake()


# In[15]:


print(model)

