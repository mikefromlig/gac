#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 14/Sept/2017

import math
import numpy as np

def distance(a, b):
    r = 0
    for i in  range(len(a)):
        r += (a[i]-b[i])*(a[i]-b[i])
    return math.sqrt(r)


class iso_circle:
    def __init__(self, nb, D, ID, rho):
        
        self.nb             = nb
        self.diameter       = D
        self.ID             = ID
        self.rho            = rho
        self.current_target = 0
        self.sh             = None
        self.vbos           = None
        self.model          = None
        self.positions      = []
        self.display        = True
        self.display_all    = False
        
        self.make_circle()
    
    def make_circle(self):
        
        vertices = []
        colors = []
        angle = 2*math.pi/self.nb
        
        for i in range(self.nb):
            x = math.cos(i*angle)*self.diameter/2.0
            y = math.sin(i*angle)*self.diameter/2.0
            self.positions.append([x, y, 0, 1])
            
        self.amplitude = distance(self.positions[0], self.positions[int((self.nb)/2)])
        self.width     = self.amplitude/(2**self.ID - 1)
        
        for i in range(self.nb):
            color = [0, 1, 1, 0]
            if self.display_all:
                color = [1, 0, 0, .3]
            if i == self.current_target:
                    color = [0, 1, 0, 1]
            t, c = circle(self.positions[i][:3], self.width/2.0, 20, color, 1)
            vertices.extend(t)
            colors.extend(c)
            
        self.model = [np.array(vertices), np.array(colors)]
    
    
    def next(self):
        self.current_target = (self.current_target + int(self.nb/2)) % self.nb
    
    
    #m: mouse position ; r: target radius
    def is_current_clicked(self, m, mp, mm, w, h):
    
        def distance2D(a, b):
            return math.sqrt((a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1]))
        
        #target_center
        pc = mp.dot(mm.dot(np.array(self.positions[self.current_target])))
        pc = pc/pc[3]
        pc = pc/pc[2]
        pc = [w*(pc[0]+1)/2.0, h*(pc[1]+1)/2.0]
        
        #target_edge
        edge = np.array(self.positions[self.current_target]) + np.array([1, 0, 0, 0])*self.width/2.0
        pe = mp.dot(mm.dot(edge))
        pe = pe/pe[3]
        pe = pe/pe[2]
        pe = [w*(pe[0]+1)/2.0, h*(pe[1]+1)/2.0]
        
        dtm = distance2D(pc, m)
        r   = distance2D(pe, pc)
        
        if dtm <= r:
            return 1
        else:
            return 0


def circle(p, r, nb_arcs, color, ratio):
    angle = 2*math.pi/nb_arcs
    arr, col = [], []
    for i in range(nb_arcs):
        x1 = math.cos(i*angle)*r
        y1 = math.sin(i*angle)*r*ratio
        x2 = math.cos((i+1)*angle)*r
        y2 = math.sin((i+1)*angle)*r*ratio
        
        arr.append(np.array([0,    0,  0])+p)
        arr.append(np.array([x1,   y1, 0])+p)
        arr.append(np.array([x2,   y2, 0])+p)
        col.append(color)
        col.append(color)
        col.append(color)
    return np.array(arr), np.array(col)


