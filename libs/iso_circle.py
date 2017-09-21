#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 14/Sept/2017

import math
import numpy as np

class iso_circle:
    def __init__(self, nb, d, w):
        
        self.nb             = nb
        self.amplitude      = d
        self.current        = 0
        self.width          = w
        self.sh             = None
        self.vbos           = None
        self.model          = None
        self.positions      = []
        self.display        = True
        self.display_all    = True
    
    
    def make_circle(self):
        
        vertices = []
        colors = []
        angle = 2*math.pi/self.nb
        
        for i in range(self.nb):
            x = math.cos(i*angle)*self.amplitude/2.0
            y = math.sin(i*angle)*self.amplitude/2.0
            if self.display_all:
                color = [1, 0, 0, .3]
            else:
                color = [0, 1, 1, 0]
            if i == self.current:
                    color = [0, 1, 0, 1]
            t, c = circle([x, y, 0], self.width/2.0, 20, color)
            vertices.extend(t)
            colors.extend(c)
            self.positions.append([x, y, 0, 1])
        
        self.model = [np.array(vertices), np.array(colors)]
    
    
    def next(self):
        self.current = (self.current + int(self.nb/2)) % self.nb
    
    
    #m: mouse position ; r: target radius
    def is_current_clicked(self, m, mp, mm, w, h):
    
        def distance2D(a, b):
            return math.sqrt((a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1]))
        
        #target_center
        pc = mp.dot(mm.dot(np.array(self.positions[self.current])))
        pc = pc/pc[3]
        pc = pc/pc[2]
        pc = [w*(pc[0]+1)/2.0, h*(pc[1]+1)/2.0]
        
        #target_edge
        edge = np.array(self.positions[self.current]) + np.array([1, 0, 0, 0])*self.width/2.0
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


def circle(p, r, nb_arcs, color):
    angle = 2*math.pi/nb_arcs
    arr, col = [], []
    for i in range(nb_arcs):
        x1 = math.cos(i*angle)*r
        y1 = math.sin(i*angle)*r
        x2 = math.cos((i+1)*angle)*r
        y2 = math.sin((i+1)*angle)*r
        
        arr.append(np.array([0,    0,  0])+p)
        arr.append(np.array([x1,   y1, 0])+p)
        arr.append(np.array([x2,   y2, 0])+p)
        col.append(color)
        col.append(color)
        col.append(color)
    return np.array(arr), np.array(col)


