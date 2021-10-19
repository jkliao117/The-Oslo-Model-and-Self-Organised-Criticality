#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 16:56:54 2019

@author: RoroLiao
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
from complexity import Lattice, Ensemble
import scipy.stats as sps

"""task 2e"""
# import data
Llist = [4,8,16,32,64,128,256]
avgh_list = np.loadtxt('avgh.txt')

# fit and find parameters
def function(L,a0,a1,omega1):
    return a0 * L * (1 - a1 * (L ** (-omega1)))
fit = spo.curve_fit(function,Llist,avgh_list)
value = fit[0]
error = fit[1]
a0 = value[0]
a1 = value[1]
omega1 = value[2]
print ('a0=', a0, 'a1=', a1, 'omega1=', omega1)
print ('a0 error=', error[0][0]**0.5, 'a1 error=', error[1][1]**0.5, 'omega1 error=', error[2][2]**0.5)

# plot <h> vs L
fit_avgh_list = function(np.asarray(Llist),a0,a1,omega1)
fig = plt.figure()
plt.plot(Llist,avgh_list,'ro')
plt.plot(Llist,fit_avgh_list,'salmon')
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'systen size L')
plt.ylabel(r'average height $\langle h(t;L)\rangle_t$')
plt.legend(['experimental data',r'fit function $a_0L(1-a_1L^{-\omega_1})$'])

# # evaluate the goodness of fit by chi squared test
print ('average percentage difference =', np.mean((avgh_list - fit_avgh_list)/fit_avgh_list))
chi_squared, p = sps.chisquare(avgh_list, fit_avgh_list)
print('chi_squared=', chi_squared, 'p value=',p)