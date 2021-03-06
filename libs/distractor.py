#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 06/Oct/2017

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
    if n == 0:
        return [0, 0, 0]
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
    
    nb_before = int(len(iso_IDS)/2)
    
    #higher than A
    i=1
    nA, nW = compute_a_w(ID, A, rho, 1)
    while nA < maxA:
        iso_IDS = np.append(iso_IDS, [nA, nW])
        i += 1
        nA, nW = compute_a_w(ID, A, rho, i)
    
    return iso_IDS.reshape(int(len(iso_IDS)/2), 2), nb_before


def thick_circle(radius, thickness, depth, tess, color):
    angle = 2*math.pi/tess
    vertices = []
    colors = []
    normals = []
    
    for i in range(tess):
        xl1 = math.cos(i*angle)*(radius-thickness/2.0)
        xl2 = math.cos((i+1)*angle)*(radius-thickness/2.0)
        xr1 = math.cos(i*angle)*(radius+thickness/2.0)
        xr2 = math.cos((i+1)*angle)*(radius+thickness/2.0)
        
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
        if len(top1):
            l1 = top1[0][i*6+1]
            l2 = top1[0][i*6+2]
        else:
            l1 = [0, 0, 0]
            l2 = [0, 0, 0]
        
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


def make_distractor(id, amplitude, rho, targets_width):
    
    # distractors positions (circle radius and width)
    iso_IDs, nb_before = compute_iso_IDS(id, amplitude, rho, targets_width/2.0, 20)
    
    vertices, colors, normals = [], [], []
    tops = []
    inters = []
    for i in range(len(iso_IDs)):
        
        # depth equations: 
        # - y = x/20 till the middle
        # - y = middle - x/20 till the target
        depth = iso_IDs[i][0]/5.
        if i%2 and nb_before%2 == 0:
            depth = 0
        elif not i%2 and nb_before%2:
            depth = 0
        
        tess = 200
        tops.append(thick_circle(iso_IDs[i][0], iso_IDs[i][1], depth, tess, [1,1,1,1]))
    
    inters.append(inter_circle([], tops[0], tess, [1,1,1,1]))
    for i in range(len(iso_IDs)-1):
        inters.append(inter_circle(tops[i], tops[i+1], tess, [1,1,1,1]))
    
    for t,i in zip(tops, inters):
        vertices.extend(t[0])
        colors.extend(t[1])
        normals.extend(t[2])
        
        vertices.extend(i[0])
        colors.extend(i[1])
        normals.extend(i[2])
    
    return [np.array(vertices), np.array(colors), np.array(normals)]

