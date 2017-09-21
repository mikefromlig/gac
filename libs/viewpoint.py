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


def m_rotation(vector, angle):
    v = v_normalize(vector)
    s = math.sin(angle)
    c = math.cos(angle)
    C = 1 - c
    
    sx = s * v[0]
    sy = s * v[1]
    sz = s * v[2]
    Cx = C * v[0]
    Cy = C * v[1]
    Cz = C * v[2]
    Cxy = Cy * v[0]
    Cyz = Cz * v[1]
    Czx = Cx * v[2]
    
    return numpy.array([v[0] * Cx + c,      Cxy - sz,       Czx + sy,       0.0,
                       Cxy + sz,            v[1] * Cy + c,  Cyz - sx,       0.0,
                       Czx - sy,            Cyz + sx,       v[2] * Cz + c,  0.0,
                       0.0,                 0.0,            0.0,            1.0]).reshape((4,4))


def rotate(p, vector, angle, pivot = []):
    
    M = m_rotation(vector, angle)
    
    if len(pivot) == 0:
        return M.dot(numpy.array([p[0], p[1], p[2], 1.0]))[:3]
    else:
        po = numpy.array([p[0], p[1], p[2], 1.0])
        pi = numpy.array([pivot[0], pivot[1], pivot[2], 1.0])
        return (M.dot( po - pi) +pi)[:3]


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
    
    rfov = fov*math.pi/180.
    d = 1/math.tan(rfov/2.)
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
