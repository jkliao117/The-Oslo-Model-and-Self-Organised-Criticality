#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 12:28:21 2019

@author: RoroLiao
"""

import matplotlib.pyplot as plt
import numpy as np
from complexity import Lattice, Ensemble
import scipy.stats as sps

"""task 2d"""
# import data
Llist = [4,8,16,32,64,128,256]
total_time = 1e5
tc_s_list = np.loadtxt('tc_s.txt')

# find the average slope <zi> using eq(1) h = L * avg_zth in steady state
def find_avg_z(L,est_tc,trial):
    # create lattice
    Ltc = Lattice(L,0.5)
    # run the system until it reaches steay state
    Ltc.Oslo(est_tc)
    # periodically sample average zi in steady state
    zlist = []
    for i in range(trial):
        # sample once every 10 times
        Ltc.additional_Oslo(1)
        # <z>=h/L
        zlist.append(Ltc.get_h1()/L)
    # calculate the avergae z
    avg_z = np.mean(zlist)
    std_z = np.std(zlist)
    return avg_z, std_z

# find the average slope <zi> for all lattices
def avgz_func(Llist,tc_s_list):
    avgz_list = []
    for i in range(len(Llist)):
        z = find_avg_z(Llist[i],int(tc_s_list[i]),100)[0]
        avgz_list.append(z)
    return avgz_list

avgz_list = avgz_func(Llist,tc_s_list)

# compute the theoretical corss over time tc
def theoretical_tc_func(Llist,avgz_list):
    theoretical_tc_list = []
    for i in range(len(Llist)):
        theoretical_tc = (avgz_list[i]/2)*(Llist[i]**2)*(1+(1/Llist[i]))
        theoretical_tc_list.append(theoretical_tc)
    return theoretical_tc_list

theoretical_tc_s_list = theoretical_tc_func(Llist,avgz_list)

# plot <t_c> vs L
fig = plt.figure()
plt.plot(Llist,tc_s_list,'go')
plt.plot(Llist,theoretical_tc_s_list,'springgreen')
plt.xlabel(r'system size L')
plt.ylabel(r'average cross-over time $\langle t_c \rangle$')
plt.legend([r'experimental data',r'theoretical prediction $\frac{\langle z\rangle}{2}L^2(1+\frac{1}{L})$'])
plt.xscale('log')
plt.yscale('log')

# evaluate the goodness of fit by chi squared test
print ('average percentage difference =', np.mean((tc_s_list - theoretical_tc_s_list)/theoretical_tc_s_list))
chi_squared, p = sps.chisquare(tc_s_list, theoretical_tc_s_list)
print('chi_squared=', chi_squared, 'p value=',p)