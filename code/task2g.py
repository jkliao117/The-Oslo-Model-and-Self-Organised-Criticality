#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 10:30:57 2019

@author: RoroLiao
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
import scipy.stats as sps

"""task 2g"""
# import data
Llist = [4,8,16,32,64,128,256]
h_list = np.loadtxt('h.txt')
tc_list = np.loadtxt('tc.txt')
avgh_list = np.loadtxt('avgh.txt')
hstd_list = np.loadtxt('hstd.txt')

# sample h after tc
def h_after_crossover(h_list,tc_list):
    h_tc_list = np.zeros(h_list.shape)
    for i in range(len(Llist)):
        h_tc_list[i][int(tc_list[i]):int(tc_list[i]+4e4)] = h_list[i][int(tc_list[i]):int(tc_list[i]+4e4)]
    return h_tc_list

h_tc_list = h_after_crossover(h_list,tc_list)        

# plot probability distibution of h 
fig = plt.figure()
peak_p = np.zeros(len(Llist))
peak_h = np.zeros(len(Llist))
for i in range(len(Llist)):
    data = np.trim_zeros(h_tc_list[i])
    bins,counts = np.unique(data,return_counts=True)
    plt.plot(bins,counts/sum(counts))
    peak_h[i] = max(counts/sum(counts))
    peak_p[i] = bins[np.where(counts==max(counts))]
plt.legend(['4','8','16','32','64','128','256'])
plt.xlabel('height h')
plt.ylabel('height probability P(h;L)')

# check if peak height vs L relation is consistent with sigma_h vs L
def fit_log(list0, list1):
    loglist0 = [np.log(i) for i in list0] 
    loglist1 = [np.log(i) for i in list1] 
    fit = np.polyfit(loglist0,loglist1,1,cov=True)
    print ('value=',fit[0])
    print ('cov=',fit[1])
    fit_fn = np.poly1d(fit[0])
    fit_output = [np.exp(fit_fn[1])*(i**fit_fn[0]) for i in list0]
    return fit_output,fit[0],fit[1]
fit = fit_log(Llist,peak_h)
fit_peakh_list = np.exp(fit[1][1])*(Llist**fit[1][0])
print('L vs peak_h exponent=', fit[1][0], fit[2][0][0]**0.5)
fig = plt.figure()
plt.plot(Llist,peak_h)
plt.plot(Llist,fit_peakh_list)
plt.xlabel('system size L')
plt.ylabel('peak height of P(h;L)')
    
# data collapse    
fig = plt.figure()
X = np.zeros([0,0])
Y = np.zeros([0,0])
for i in range(len(Llist)):
    data = np.trim_zeros(h_tc_list[i])
    bins,counts = np.unique(data,return_counts=True)
    bins1 = (bins-avgh_list[i])/hstd_list[i]
    counts1 = counts*hstd_list[i]/sum(counts)
    plt.scatter(bins1,counts1,s=3)
    X = np.concatenate((X,bins1),axis=None)
    Y = np.concatenate((Y,counts1),axis=None)

# gaussian fit for data collapse
Y = Y[np.argsort(X)]
X = np.sort(X)
mean = 0
std = 1
x = np.arange(min(X),max(X),0.01)
def Gaussian(h,mean,std):
    a = 1/(np.sqrt(2*np.pi)*std)
    b = ((h-mean)/std)**2
    c = a*np.exp(-0.5*b)
    return c
plt.legend(['4','8','16','32','64','128','256'])
plt.xlabel(r'height $(h - \langle h\rangle)/\sigma_h$')
plt.ylabel(r'height probability $\sigma_hP(h;L)$')
plt.plot(x,Gaussian(x,mean,std),label = r'$\mu$ = 0, $\sigma$ = 1')

# evaluate the goodness of fit by chi squared test
chi_squared, p = sps.chisquare(Y, Gaussian(X,mean,std))
print('chi_squared=', chi_squared, 'p value=',p)



    