#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:17:20 2019

@author: RoroLiao
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
from complexity import Lattice, Ensemble
import scipy.stats as sps

"""task 2b"""
# import data
Llist = [4,8,16,32,64,128,256]
total_time = 1.6e5
tc_s_list = np.loadtxt('tc_s.txt')
avgh_list = np.loadtxt('avgh.txt')

# calculate the power byt using 1D fit on log-log plot        
def fit_log(list0, list1):
    loglist0 = [np.log(i) for i in list0] 
    loglist1 = [np.log(i) for i in list1] 
    fit = np.polyfit(loglist0,loglist1,1,cov=True)
    #print ('A=',np.exp(fit[0[0]]),'n=',fit[0][1])
    print ('value=',fit[0])
    print ('cov=',fit[1])
    fit_fn = np.poly1d(fit[0])
    fit_output = [np.exp(fit_fn[0])*(i**fit_fn[1]) for i in list0]
    return fit_output

# plot <h> vs L
fig = plt.figure()
plt.plot(Llist, avgh_list, 'ro')
fit1 = fit_log(Llist,avgh_list)
fit11 = fit_log(Llist[2:],avgh_list[2:])
plt.plot(Llist, fit1, 'Salmon')
plt.xlabel(r'system size L')
plt.ylabel(r'avergae height $ \langle h(t,L) \rangle_t $')
plt.xscale('log')
plt.yscale('log')
plt.legend(['experimental data','linear fit'])

# evaluate the goodness of fit bu chi squared test
chi_squared, p = sps.chisquare(avgh_list[2:], fit1[2:])
print('chi_squared=', chi_squared, 'p value=',p)

# plot <tc> vs L
fig = plt.figure()
plt.plot(Llist, tc_s_list, 'bo')
fit2 = fit_log(Llist,tc_s_list)
fit22 = fit_log(Llist[2:],tc_s_list[2:])
plt.plot(Llist,fit2,'DarkCyan')
plt.xlabel(r'system size L')
plt.ylabel(r'average cross-over time $\langle t_c \rangle$')
plt.xscale('log')
plt.yscale('log')
plt.legend(['experimental data','linear fit'])

# evaluate the goodness of fit by chi squared test
chi_squared, p = sps.chisquare(tc_s_list[2:],fit2[2:])
print('chi_squared=', chi_squared, 'p value=',p)