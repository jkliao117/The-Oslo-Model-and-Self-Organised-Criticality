#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 11:33:59 2019

@author: RoroLiao
"""
import matplotlib.pyplot as plt
import numpy as np
from logbin import logbin

"""task 3a"""
# import data
Llist = [4,8,16,32,64,128,256]
s_list = np.loadtxt('s.txt')
tc_s_list = np.loadtxt('tc_s.txt')

# sample avalanche size for the first 10^5 unit time after the cross over time
def s_after_crossover(s_list,tc_list):
    s_tc_list = np.zeros((len(s_list),int(1e5)))
    for i in range(len(Llist)):
        s_tc_list[i] = s_list[i][int(tc_list[i]):int(tc_list[i]+1e5)]
    return s_tc_list

s_tc_list = s_after_crossover(s_list,tc_s_list).astype(int)

# plot probability distribution using log-binned data (scale=1)
fig = plt.figure()        
for i in range(len(Llist)):
    data = np.trim_zeros(s_tc_list[i])
    x,y = logbin(data,scale = 1)
    plt.scatter(x,y,s=5)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(['4','8','16','32','64','128','256'])
    plt.xlabel('avalanche size s')
    plt.ylabel('avalanche size probability P(s;L)')

# plot probability distribution using log-binned data (scale=1)
fig = plt.figure()        
for i in range(len(Llist)):
    data = np.trim_zeros(s_tc_list[i])
    x,y = logbin(data,scale = 1.5)
    plt.plot(x,y)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(['4','8','16','32','64','128','256'])
    plt.xlabel('avalanche size s')
    plt.ylabel('avalanche size probability P(s;L)')
    
