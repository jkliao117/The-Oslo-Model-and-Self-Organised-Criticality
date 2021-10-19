#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:17:57 2019

@author: RoroLiao
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
import scipy.stats as sps
from logbin import logbin

"""task 3c"""
# import data 
Llist = [4,8,16,32,64,128,256]
k_list = [1,2,3,4]
s_list = np.loadtxt('s.txt')
tc_s_list = np.loadtxt('tc_s.txt')

# sample avalanche size for the first 10^5 unit time after the cross over time
def s_after_crossover(s_list,tc_list):
    s_tc_list = np.zeros((len(s_list),int(1e5)))
    for i in range(len(Llist)):
        s_tc_list[i] = s_list[i][int(tc_list[i]):int(tc_list[i]+1e5)]
    return s_tc_list

s_tc_list = s_after_crossover(s_list,tc_s_list)

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
    return fit_output, fit[0]

# calculate <s^k>
sk_list = np.zeros([len(Llist),len(k_list)])
for j in range(len(k_list)):
    k = k_list[j]
    for i in range(len(Llist)):
        data = (s_tc_list[i])**k
        sk_list[i][j]= np.mean(data)
sk_list = np.transpose(sk_list)

# plot <s^k> vs L
fig = plt.figure()
for i in range(len(k_list)): 
    plt.plot(Llist,sk_list[i],'-o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('system size L')
plt.ylabel(r'$k_{th}$ moment average avalanche size $\langle s^k \rangle$')
plt.legend(['1','2','3','4'])

# find the slope D(1+k-tau) for <s^k> vs L on log scale
exponent_list = [] 
for j in range(len(k_list)):
    exponent = fit_log(Llist,sk_list[j])[1][0]
    exponent_list.append(exponent)

# fit and find parameters
def function(k,D,tau):
    return D*(1+k-tau)
fit = spo.curve_fit(function,k_list,exponent_list)
value = fit[0]
error = fit[1]
D = value[0]
tau = value[1]
print ('D=', D, 'tau=', tau)
print ('D error=', error[0][0]**0.5, 'tau error=', error[1][1]**0.5)

# plot D(1+k-tau) vs k
fit_exponent_list = D*(1+np.asarray(k_list)-tau)
fig = plt.figure() 
plt.plot(k_list,exponent_list,'go')
plt.plot(k_list,fit_exponent_list,'LimeGreen')
plt.xlabel('k')
plt.ylabel(r'$D(1+k-\tau_s)$')
plt.legend(['experimental data',r'fit function $D(1+k-\tau_s)$'])

# evaluate the goodness of fit by chi squared test
chi_squared, p = sps.chisquare(exponent_list, fit_exponent_list)
print('chi_squared=', chi_squared, 'p value=',p)

# consistency check
print (D*(2-tau))