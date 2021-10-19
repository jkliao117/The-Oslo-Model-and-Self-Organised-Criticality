#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:15:50 2019

@author: RoroLiao
"""

import matplotlib.pyplot as plt
import numpy as np
from complexity import Lattice, Ensemble
import scipy.stats as sps

"""task 2a"""
# import data
Llist = [4,8,16,32,64,128,256]
total_time = 1.6e5
h_list = np.loadtxt('h.txt')
tc_s_list = np.loadtxt('tc_s.txt')
 
# plot h vs t graph     
fig = plt.figure()
for i in range(len(Llist)):
    plt.plot(np.arange(total_time+1),h_list[i])
    plt.vlines(x=tc_s_list[i],ymin=0,ymax=h_list[i][int(tc_s_list[i])],linestyles='dashed')
plt.legend(['L=4','L=8','L=16','L=32','L=64','L=128','L=256'])
plt.xlabel(r'time t')
plt.ylabel(r'height h(t;L)')
#plt.xscale('log')
#plt.yscale('log')

# find slope of log-log graphs
def fit_log(list0, list1):
    loglist0 = [np.log(i) for i in list0] 
    loglist1 = [np.log(i) for i in list1] 
    fit = np.polyfit(loglist0,loglist1,1,cov=True)
    print ('value=',fit[0])
    print ('cov=',fit[1])
    fit_fn = np.poly1d(fit[0])
    fit_output = [np.exp(fit_fn[1])*(i**fit_fn[0]) for i in list0]
    return fit_output,fit[0],fit[1]

# find the relations between tc and hc
# get hc
hc_s_list = []
for i in range(len(Llist)):
    hc_s_list.append(np.mean(h_list[i][int(tc_s_list[i]):int(tc_s_list[i]+100)]))

#plot hc vs tc
fig = plt.figure()
plt.plot(tc_s_list,hc_s_list,'go')
fit1 = fit_log(tc_s_list,hc_s_list)
fit_hc_s_list = np.exp(fit1[1][1])*(tc_s_list**fit1[1][0])
print('hc vs tc, exponent=', fit1[1][0], fit1[2][0][0]**0.5)
plt.plot(tc_s_list,fit_hc_s_list,'limegreen')
plt.legend(['experimental data','linear fit'])
plt.xlabel(r'cross-over time $t_c$')
plt.ylabel(r'cross-over height $h_c$')
plt.xscale('log')
plt.yscale('log')

# evaluate the goodness of fit by chi squared test
chi_squared, p = sps.chisquare(hc_s_list, fit_hc_s_list)
print('chi_squared=', chi_squared, 'p value=',p)