#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import sys
import math
import numpy as np


def compute_a_w(ID, A, rho, i):
    Ai = A*(1 + 1/((2**ID - 1)*rho - 1/2))**i
    return Ai, Ai/(2**ID - 1)


def compute_iso_IDS(ID, A, rho, minA, maxA):
    
    iso_IDS = np.array([])
    
    #lower than A
    i = 0
    nA, nW = compute_a_w(ID, A, rho, 0)
    while nA > minA:
        iso_IDS = np.append([nA, nW], iso_IDS)
        i -= 1
        nA, nW = compute_a_w(ID, A, rho, i)
    
    #higher than A
    i=1
    nA, nW = compute_a_w(ID, A, rho, 1)
    while nA < maxA:
        iso_IDS = np.append(iso_IDS, [nA, nW])
        i += 1
        nA, nW = compute_a_w(ID, A, rho, i)
    
    return iso_IDS.reshape((len(iso_IDS)/2), 2)


def thick_circle(radius, thickness, steps, color):
    angle = 2*math.pi/steps
    vertices = []
    colors = []
    for i in range(steps):
        xl1 = math.cos(i*angle)*(radius-thickness/2.0)+4
        xl2 = math.cos((i+1)*angle)*(radius-thickness/2.0)+4
        xr1 = math.cos(i*angle)*(radius+thickness/2.0)+4
        xr2 = math.cos((i+1)*angle)*(radius+thickness/2.0)+4
        
        yl1 = math.sin(i*angle)*(radius-thickness/2.0)
        yl2 = math.sin((i+1)*angle)*(radius-thickness/2.0)
        yr1 = math.sin(i*angle)*(radius+thickness/2.0)
        yr2 = math.sin((i+1)*angle)*(radius+thickness/2.0)
        
        vertices.extend([[xl1, yl1, -0.01], [xr1, yr1, -0.01], [xr2, yr2, -0.01]])
        vertices.extend([[xl1, yl1, -0.01], [xr2, yr2, -0.01], [xl2, yl2, -0.01]])
        for i in range(6):
            colors.extend(color)
        
    return vertices, colors
    

class object:
    def __init__(self, file=None, _iso_circle=None):
        self.sh         = None
        self.vbos       = None
        self.model      = None
        self.display    = True
        
        if not file:
            self.model = self.make_distractor(_iso_circle, 5)
        else:
            print("Obj parser not implemented yet !!!")
            sys.exit()
        
    def make_distractor(self, iso_circle, nb_waves):
        
        iso_IDs = compute_iso_IDS(iso_circle.ID, iso_circle.amplitude, iso_circle.rho, iso_circle.width/2.0, 30)
        
        vertices    = [ [-5, -5, -1], [5, -5, -1],    [5, 5, -1], 
                        [-5, -5, -1], [5, 5, -1],     [-5, 5, -1] ]
                        
        colors      = [ [1, 1, 0.2, 1], [1, 1, 0.2, 1], [1, 0, 0.2, .5],
                        [1, 1, 0.2, 1], [1, 0, 0.2, .5], [1, 0, 0.2, .5]]
        
        '''
        vertices, colors = [], []
        for iso in iso_IDs:
            v, c = thick_circle(iso[0], iso[1], 50, [0,0,1,.3])
            vertices.extend(v)
            colors.extend(c)
        '''    
        return [np.array(vertices), np.array(colors)]
    