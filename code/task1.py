#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:14:21 2019

@author: RoroLiao
"""

import matplotlib.pyplot as plt
import numpy as np
from complexity import Lattice, Ensemble

"""task1"""

# find the change of h1 against time and get the aveage after cross over time
def find_h1(L,p,t):
    # create lattice
    Ltc = Lattice(L,p)
    # run simulation
    Ltc.Oslo(t)
    # calculate the average height
    Ltc.h1_avg()
    return Ltc._h1list, Ltc._h1_avg, Ltc._h1_avg_std, Ltc._tc

# for BTW with zth=2, zth=1 for L=16
L16_BTW0_h1list, L16_BTW0_avgh1, L16_BTW0_h1std, L16_BTW0_tc = find_h1(16,0,5e2)
L16_BTW1_h1list, L16_BTW1_avgh1, L16_BTW1_h1std, L16_BTW1_tc= find_h1(16,1,5e2)
print ("L=16 in BTW (zth=2) model=", L16_BTW0_avgh1, L16_BTW0_h1std)
print ("L=16 in BTW (zth=1) model=", L16_BTW1_avgh1, L16_BTW1_h1std)

# plot h vs t (BTW p=0, p=1 for L=16)
t = np.arange(0,5e2+1)
fig1 = plt.figure()
plt.plot(t, L16_BTW0_h1list, label = 'L=16,p=0')
plt.plot(t, L16_BTW1_h1list, label = 'L=16,p=1')
plt.legend(loc = 4)
plt.xlabel('time t')
plt.ylabel('height h(t,L=16)')


# for Oslo p = 0.5 for L=8, L=16, L=32
L8_Oslo_h1list, L8_Oslo_avgh1, L8_Oslo_h1std, L8_Oslo_tc = find_h1(8,0.5,5e3)
L16_Oslo_h1list, L16_Oslo_avgh1, L16_Oslo_h1std, L16_Oslo_tc = find_h1(16,0.5,5e3)
L32_Oslo_h1list, L32_Oslo_avgh1, L32_Oslo_h1std, L32_Oslo_tc = find_h1(32,0.5,5e3)
print ("L=8 in Oslo model=", L8_Oslo_avgh1, L8_Oslo_h1std)
print ("L=16 in Oslo model=", L16_Oslo_avgh1, L16_Oslo_h1std)
print ("L=32 in Oslo model=", L32_Oslo_avgh1, L32_Oslo_h1std)

# plot h vs t (Oslo p=0.5 for L=16, L=32)
t = np.arange(0,2e3)
fig2 = plt.figure()
plt.plot(t, L8_Oslo_h1list[0:2000], label = 'L=8,p=0.5')
plt.plot(t, L16_Oslo_h1list[0:2000], label = 'L=16,p=0.5')
plt.plot(t, L32_Oslo_h1list[0:2000], label = 'L=32,p=0.5')
plt.legend(loc = 4)
plt.xlabel('time t')
plt.ylabel('height h(t,L)')

# find the average zth using eq(1) h = L * avg_zth in steady state
def find_avg_z(L,p,est_tc,trial):
    # create lattice
    Ltc = Lattice(L,p)
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

# for Oslo p = 0.5 for L=8, L=16, L=32
L8_Oslo_avgz, L8_Oslo_zstd = find_avg_z(8,0.5,L16_Oslo_tc,1000)
L16_Oslo_avgz, L16_Oslo_zstd = find_avg_z(16,0.5,L16_Oslo_tc,1000)
L32_Oslo_avgz, L32_Oslo_zstd = find_avg_z(32,0.5,L32_Oslo_tc,1000)
print ("average zth for Oslo L=8 =", L8_Oslo_avgz, L8_Oslo_zstd)
print ("average zth for Oslo L=16 =", L16_Oslo_avgz, L16_Oslo_zstd)
print ("average zth for Oslo L=32 =", L32_Oslo_avgz, L32_Oslo_zstd)