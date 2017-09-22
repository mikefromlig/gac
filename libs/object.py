#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import sys
import math
import numpy as np


def compute_a_w(ID, A, rho, i):
    Ai = A*(1 + 1/((2**ID - 1)*rho - 1/2))**i
    return Ai, Ai/(2**ID - 1)


def vector3(a, b):
    return [ b[0] - a[0], b[1] - a[1], b[2] - a[2] ]


def cross(u, v):
    return [    u[1]*v[2] - u[2]*v[1],
                u[2]*v[0] - u[0]*v[2],
                u[0]*v[1] - u[1]*v[0]   ]


def normalize(u):
    n = math.sqrt(u[0]*u[0] + u[1]*u[1] + u[2]*u[2])
    return [u[0]/n, u[1]/n, u[2]/n]


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


def thick_circle(radius, thickness, depth, tess, color):
    angle = 2*math.pi/tess
    vertices = []
    colors = []
    normals = []
    
    for i in range(tess):
        xl1 = math.cos(i*angle)*(radius-thickness/2.0)+4
        xl2 = math.cos((i+1)*angle)*(radius-thickness/2.0)+4
        xr1 = math.cos(i*angle)*(radius+thickness/2.0)+4
        xr2 = math.cos((i+1)*angle)*(radius+thickness/2.0)+4
        
        yl1 = math.sin(i*angle)*(radius-thickness/2.0)
        yl2 = math.sin((i+1)*angle)*(radius-thickness/2.0)
        yr1 = math.sin(i*angle)*(radius+thickness/2.0)
        yr2 = math.sin((i+1)*angle)*(radius+thickness/2.0)
        
        vertices.extend([[xl1, yl1, depth-0.01], [xr1, yr1, depth-0.01], [xr2, yr2, depth-0.01]])
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        vertices.extend([[xl1, yl1, depth-0.01], [xr2, yr2, depth-0.01], [xl2, yl2, depth-0.01]])
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        for i in range(6):
            colors.extend(color)
        
    return vertices, colors, normals


def inter_circle(top1, top2, tess, color):
    
    vertices = []
    colors = []
    normals = []
    
    for i in range(tess):
        l1 = top1[0][i*6+1]
        l2 = top1[0][i*6+2]
        
        r1 = top2[0][i*6]
        r2 = top2[0][i*6+5]
        
        vertices.extend([l1, r1, r2])
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        vertices.extend([l1, r2, l2])
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        normals.extend(normalize(cross(vector3(vertices[-2], vertices[-3]), vector3(vertices[-1], vertices[-3]))))
        for i in range(6):
            colors.extend(color)
    
    return vertices, colors, normals

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
        
        # distractors positions (circle radius and width)
        iso_IDs = compute_iso_IDS(iso_circle.ID, iso_circle.amplitude, iso_circle.rho, iso_circle.width/2.0, 20)
        
        vertices    = [ [-5, -5, -1], [5, -5, -1],    [5, 5, -1], 
                        [-5, -5, -1], [5, 5, -1],     [-5, 5, -1] ]
                        
        colors      = [ [1, 1, 0.2, 1], [1, 1, 0.2, 1], [1, 0, 0.2, .5],
                        [1, 1, 0.2, 1], [1, 0, 0.2, .5], [1, 0, 0.2, .5]]
        normals     = [ [1, 1, 1], [1, 1, 1], [1, 1, 1],
                        [1, 1, 1], [1, 1, 1], [1, 1, 1]]
        '''
        vertices, colors, normals = [], [], []
        tops = []
        inters = []
        for i in range(len(iso_IDs)):
            
            # depth equations: 
            # - y = x/20 till the middle
            # - y = middle - x/20 till the target
            depth = iso_IDs[i][0]/15.
            if i%2:
                depth = 0
            
            tess = 200
            tops.append(thick_circle(iso_IDs[i][0], iso_IDs[i][1], depth, tess, [1,1,1,1]))
        
        for i in range(len(iso_IDs)-1):
            inters.append(inter_circle(tops[i], tops[i+1], tess, [1,1,1,1]))
        
        for t,i in zip(tops, inters):
            vertices.extend(t[0])
            colors.extend(t[1])
            normals.extend(t[2])
            
            vertices.extend(i[0])
            colors.extend(i[1])
            normals.extend(i[2])
        '''
        return [np.array(vertices), np.array(colors), np.array(normals)]
    