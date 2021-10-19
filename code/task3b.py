#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 22:59:17 2019

@author: RoroLiao
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as spi
from logbin import logbin

"""task 3b"""
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

# data collapse 
# tau =1.55, D= 2.25
tau = 1.53 #/pm0.03
D= 2.15 #/pm0.03

# plot data collapse for the probability distribution
fig = plt.figure()       
for i in range(len(Llist)):
    data = s_tc_list[i]
    x,y = logbin(data,scale = 1.5)
    plt.scatter(x/Llist[i]**D,y/x**-tau,s=5)
for i in range(len(Llist)):
    data = s_tc_list[i]
    x,y = logbin(data,scale = 1.5)
    f = spi.CubicSpline(x/Llist[i]**D,y/x**-tau)
    plt.plot(x/Llist[i]**D,f(x/Llist[i]**D))
plt.xscale('log')
plt.yscale('log')
plt.legend(['4','8','16','32','64','128','256'])
plt.xlabel(r'avalanche size $s/L^D$')
plt.ylabel(r'avalanche size probability $s^{-\tau_s}P(s;L)$')

# consistency check
print (D*(2-tau))
