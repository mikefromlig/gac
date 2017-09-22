#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import sys
import math
import numpy as np


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
        
        def compute_a_w(ID, A, rho, i):
            Ai = A*(1 + 1/((2**ID - 1)*rho - 1/2))**i
            return [Ai, Ai/(2**ID - 1)]
        
        vertices    = [ [-5, -5, -1], [5, -5, -1],    [5, 5, -1], 
                        [-5, -5, -1], [5, 5, -1],     [-5, 5, -1] ]
                        
        colors      = [ [1, 1, 0.2, 1], [1, 1, 0.2, 1], [1, 0, 0.2, .5],
                        [1, 1, 0.2, 1], [1, 0, 0.2, .5], [1, 0, 0.2, .5]]
        return [np.array(vertices), np.array(colors)]
    