#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
from pomegranate import *
import numpy as np
import bnlearn as bn


# In[18]:


df = pd.read_csv("sonar_data.csv")

df.head()


# In[21]:


edges = [
    ('z', 'a'),
    ('a', 'd')
]

#Create Bayesian DAG
DAG = bn.make_DAG(edges)


# In[23]:


bn.plot(DAG)


# In[25]:


DAG = bn.parameter_learning.fit(DAG, df, methodtype='maximumlikelihood')


# In[26]:


CPD = bn.print_CPD(DAG)


# In[28]:


q1 = bn.inference.fit(DAG, variables=["d"], evidence={'z':1})

