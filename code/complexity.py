#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 22:33:58 2019

@author: RoroLiao
"""

import numpy as np
import random
import matplotlib.pyplot as plt


class Ensemble():
    
    # initialising the ensemble
    def __init__(self, Llist, p):
        # system sizes
        self._Llist = Llist
        # probability
        self._p = p
        # initialising the ensemble
        self._ensemblelist = self.ensemble_initialisation()
    
    # setting up lattices of different sizes    
    def ensemble_initialisation(self):
        l = []
        l.extend([Lattice(i,self._p) for i in self._Llist])
        return l
    
    # simulation
    def ensemble_Oslo(self, total_t):
        self._total_t = total_t
        for i in range(len(self._Llist)):
            self._ensemblelist[i].Oslo(total_t)
    # reset 
    def ensemble_reset(self):
        for i in range(len(self._Llist)):
            self._ensemblelist[i].reset()
            
"""class Lattice() represents a systme with specifed number of sites and threshold slope probabilty """ 
class Lattice():
    
    def __init__(self, L, p): 
        # system size
        self._L = L
        # probability
        self._p = p
        # initialising the lattice
        self._latticelist = self.lattice_initialisation()
        # height of the first site
        self._h1list = [0]
        # avalanche size
        self._slist = [0]
        # time
        self._t = 0
        # cross over time
        self._tc = 0
        
    def __repr__(self):
        return "Lattice: (L=%s, p=%s)" % (self._L,self._p)
	
    # creating initial lattice with zi = 0 for all i and random zth ∈ {1, 2} for all i
    def lattice_initialisation(self):
        l = [Site_1(self, 0)]
        l.extend([Sites(self, i+1) for i in range(self._L-2)])
        l.append(Site_L(self, self._L-1))
        return l
    
    # identifying all sites subject to relaxation
    def relax_sites(self):
        sites = [i for i in self._latticelist if i._z>i._zth]
        return sites
    # reset 
    def reset(self):
        self._latticelist = self.lattice_initialisation()
        self._h1list = [0]
        self._slist = [0]
        self._t = 0
        self._tc = 0
        
    # Oslo algorithm simulation
    def Oslo(self, total_t):
        self._total_t = total_t
        tc_not_set = True
        while self._t < self._total_t: 
            self._t += 1
            self._s = 0
            # drive
            self._latticelist[0].drive()   
            # relaxation 
            relaxsites = self.relax_sites()
            # relax all sites in the system before adding a new grain
            while len(relaxsites) > 0:
                for i in relaxsites:
                    i.relax()
                    self._s += 1
                relaxsites = self.relax_sites()
            # find the cross over time
            if self._latticelist[-1]._d > 0 and tc_not_set:
                self._tc = self._t-1
                tc_not_set = False
            # record height and avalanche size
            self._h1list.append(self.get_h1())
            self._slist.append(self._s)
    
    # calculate the time average of height
    def h1_avg(self):
        self._h1_avg = np.mean(self._h1list[int(self._tc):-1])
        self._h1_avg_std = np.std(self._h1list[int(self._tc):-1])
        return self._h1_avg, self._h1_avg_std
    
    # get the height for the first site
    def get_h1(self):
        return self._latticelist[0]._h     
    
"""class Sites() represents general 1d sites in the lattice system"""  
class Sites():
    
    def __init__(self, lattice, i):
        # lattice the site resides in 
        self._lattice = lattice
        # probability
        self._p = lattice._p
        # site number
        self._i = i
        # zi = 0 for all i
        self._z = 0
        # random initial threshold slopes zth ∈ {1, 2} for all i
        self._zth = self.new_zth()

    def __repr__(self):
        return "site: (i=%s,z=%s,zth=%s)" % (self._i,self._z,self._zth)
    
    # random threshold threshold slopes zth ∈ {1, 2}
    # the threshold slopes zth = 1 and 2 are chosen with probability p
    def new_zth(self):
        p0 = random.uniform(0,1)
        if p0 <= self._p:
            return 1
        else:
            return 2
    
    # relaxation 
    def relax(self):
        self._z -= 2
        self._lattice._latticelist[(self._i)-1]._z += 1
        self._lattice._latticelist[(self._i)+1]._z += 1
        # a new threshold slope zth ∈ {1,2} at random for the relaxed site only
        # reset the threshold slope zth for the sites i that have relaxed.
        self._zth = self.new_zth()
        
        
"""class Sites() represents the first site in the lattice system""" 
class Site_1(Sites):

    def __init__(self, lattice, i):
        Sites.__init__(self, lattice, i)
        # height
        self._h = 0
    
    # drive for each time unit
    def drive(self):
        self._h += 1
        self._z += 1
    
    # relaxation for the first site
    # overriding the relaxtion method for a general site
    def relax(self):
        self._h -= 1
        self._z -= 2
        self._lattice._latticelist[(self._i)+1]._z += 1
        self._zth = self.new_zth()

"""class Sites() represents the last site in the lattice system""" 
class Site_L(Sites):

    def __init__(self, lattice, i):
        Sites.__init__(self, lattice, i)
        # drop number for the number of grain leaving
        self._d = 0
    
    # relaxation for last first site
    # overriding the relaxtion method for a general site    
    def relax(self):
        self._z -= 1
        self._lattice._latticelist[(self._i)-1]._z += 1
        self._zth = self.new_zth()
        self._d += 1
    
    