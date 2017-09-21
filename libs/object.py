#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import sys
import math
import numpy as np


def distance(a, b):
    r = 0
    for i in  range(len(a)):
        r += (a[i]-b[i])*(a[i]-b[i])
    return math.sqrt(r)


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
        first_target = iso_circle.positions[0]
        second_target = iso_circle.positions[int((iso_circle.nb - 1)/2)]
        
        radius = distance(first_target, second_target)
        
        
        vertices    = [ [-5, -5, -1], [5, -5, -1],    [5, 5, -1], 
                        [-5, -5, -1], [5, 5, -1],     [-5, 5, -1] ]
                        
        colors      = [ [1, 1, 0.2, 1], [1, 1, 0.2, 1], [1, 0, 0.2, .5],
                        [1, 1, 0.2, 1], [1, 0, 0.2, .5], [1, 0, 0.2, .5]]
        return [np.array(vertices), np.array(colors)]
    