#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:32:45 2019

@author: RoroLiao
"""
import numpy as np
from complexity import Lattice, Ensemble

"""h_tilde,<tc>"""
# find avergae height h_tilde and cross over time tc over realisaitons 
def Average_Realisation(Llist,total_time):
    # create all lattices
    E = Ensemble(Llist, 0.5)
    # initialise h_tilde array, row - size, column - unit time
    h_tilde = np.zeros([len(Llist),int(total_time+1)])
    # initialise tc array, row - size, column - unit time
    tc = np.zeros([1,len(Llist)])
    # run simulation n times
    iteration = 0
    # for 100 relaisations
    while iteration < 100:
        iteration += 1
        # run simulation
        E.ensemble_Oslo(total_time)
        # for each lattice - h1lsit and tc
        # sum the values for all realisations
        for i in range(len(Llist)):
            h_tilde[i] += np.asarray(E._ensemblelist[i]._h1list)
            tc[0][i] += np.asarray(E._ensemblelist[i]._tc)
        # reset lattice for each simulation
        E.ensemble_reset()
        print(iteration)
    # calculate average
    h_tilde = h_tilde/iteration
    tc = tc/iteration
    return h_tilde, tc

Llist = [4,8,16,32,64,128,256]
total_time = 1e5

h_tilde_list, tc_list = Average_Realisation(Llist,total_time)

# save data
file = open('h_tilde.txt','w') 
np.savetxt('h_tilde.txt',h_tilde_list) 
file.close() 
file = open('tc.txt','w')
np.savetxt('tc.txt',tc_list) 
file.close() 

"""h,s,tc"""
Llist = [4,8,16,32,64,128,256]
total_time = 1.6e5+1e6
E = Ensemble(Llist, 0.5)
E.ensemble_Oslo(total_time)

# create data array
h_list = np.zeros([len(Llist),int(total_time+1)])
s_list = np.zeros([len(Llist),int(total_time+1)])
tc_s_list = []
for i in range(len(Llist)):
    h_list[i] = np.asarray(E._ensemblelist[i]._h1list)
for i in range(len(Llist)):
    s_list[i] = np.asarray(E._ensemblelist[i]._slist)
for i in range(len(Llist)):
    tc_s_list.append(E._ensemblelist[i]._tc)

# save data   
file = open('h.txt','w') 
np.savetxt('h.txt',h_list) 
file.close() 
file = open('s.txt','w') 
np.savetxt('s.txt',s_list) 
file.close() 
file = open('tc_s.txt','w') 
np.savetxt('tc_s.txt',tc_s_list) 
file.close() 

"""<h>,sigma_h"""
def avgh_func(Llist,h_list,tc_s_list):
    avgh_list = np.zeros(len(Llist))
    hstd_list = np.zeros(len(Llist))
    for i in range(len(Llist)):
        avgh_list[i] = np.mean(h_list[i][int(tc_s_list[i]):int(tc_s_list[i]+1e5)])
        hstd_list[i] = np.std(h_list[i][int(tc_s_list[i]):int(tc_s_list[i]+1e5)])
    return avgh_list, hstd_list

avgh_list, hstd_list = avgh_func(Llist,h_list,tc_s_list)

# save data 
file = open('avgh.txt','w') 
np.savetxt('avgh.txt',avgh_list) 
file = open('avgh.txt','a') 
np.savetxt('hstd.txt',hstd_list) 
file.close() 
