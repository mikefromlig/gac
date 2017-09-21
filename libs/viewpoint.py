#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 07/April/2017

import numpy
import math

def m_mult(a, b):
    i, j = 0, 0
    M = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    while i < 4:
        while j < 4:
            M[i*4 + j] = a[i*4]*b[j] + a[i*4+1]*b[j+4] + a[i*4+2]*b[j+8] + a[i*4+3]*b[j+12]
            j += 1
        i += 1
        j = 0
    
    return M


def v_normalize(v):
    try:
        n = numpy.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    except ValueError:
        print()
        print()
        print(ValueError)
        print()
        exit(0)
    return [v[0]/n, v[1]/n, v[2]/n]


def v_cross (u,v):
    return [u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0]]


def perspective(fov, aspect, near, far):
    
    d = 1/math.tan(fov/2.)
    mat = numpy.zeros((4,4))
    
    mat[0][0] = d/aspect
    mat[1][1] = d
    mat[2][2] = (near + far)/(near - far)
    mat[2][3] = 2*near*far/(near-far)
    mat[3][2] = -1
    
    return mat


def viewport(sx, sy, w, h, near, far):
    
    mat = numpy.identity(4)
    
    mat[0][0] = w/2.
    mat[0][3] = sx + w/2.
    mat[1][1] = h/2.
    mat[1][3] = sy + h/2.
    mat[2][2] = (far-near)/2.
    mat[2][3] = (far+near)/2.
    
    return mat


def orthographic(left, right, bottom, top, near, far):
    
    mat = numpy.identity(4)
    
    mat[0][0] = 2./(right-left)
    mat[0][3] = -(right+left)/(right-left)
    mat[1][1] = 2./(top-bottom)
    mat[1][3] = -(top+bottom)/(top-bottom)
    mat[2][2] = -2./(far-near)
    mat[2][3] = -(far+near)/(far-near)
    
    return mat


def look_at(eye, center, up):
    f = v_normalize([   center[0] - eye[0],
                        center[1] - eye[1],
                        center[2] - eye[2]  ])
    
    _up = v_normalize(up)
    s = v_cross(f, _up)
    u = v_cross(v_normalize(s), f)
    R = [   s[0],   u[0],   -f[0],  0,
            s[1],   u[1],   -f[1],  0,
            s[2],   u[2],   -f[2],  0,
            0,      0,      0,      1   ]
    
    T = [   1,      0,      0,      0,
            0,      1,      0,      0,
            0,      0,      1,      0,
            -eye[0],-eye[1],-eye[2], 1 ]
    return numpy.array(m_mult(T, R)).reshape((4,4)).T
