#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 19:15:46 2019

@author: RoroLiao
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
import scipy.stats as sps
"""task 2f"""
# import data
Llist = [4,8,16,32,64,128,256]
hstd_list = np.loadtxt('hstd.txt')

# fit and find parameters
def function(L,b0,omega0):
    return b0*(L**(omega0))
fit = spo.curve_fit(function,Llist,hstd_list)
value = fit[0]
error = fit[1]
b0 = value[0]
omega0 = value[1]
print ('b0=', b0,'omega0=', omega0)
print ('b0 error=', error[0][0]**0.5, 'omega0 error=', error[1][1]**0.5)

# plot sigma_h vs L
fit_hstd_list = function(np.asarray(Llist),b0,omega0)
fig = plt.figure()
plt.plot(Llist,hstd_list,'bo')
plt.plot(Llist,fit_hstd_list,'Navy')
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'systen size L')
plt.ylabel(r'standard deviation of height $\sigma_h(L)$')
plt.legend(['experimental data',r'fit function $b_0L^{-w_0}$'])

# evaluate the goodness of fit by chi squared test
print ('average percentage difference =', np.mean((hstd_list - fit_hstd_list)/fit_hstd_list))
chi_squared, p = sps.chisquare(hstd_list, fit_hstd_list)
print('chi_squared=', chi_squared, 'p value=',p)