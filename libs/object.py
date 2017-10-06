#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import sys
import math
import numpy as np


class object:
    def __init__(self, file=None):
        self.sh             = None
        self.vbos           = None
        self.model          = None
        self.display        = True
        self.displacement   = np.identity(4)
        
        if not file:
            self.model = self.make_plan()
        else:
            print("Obj parser not implemented yet !!!")
            sys.exit()
        
        
    def make_plan(self):
        
        vertices    = [ [-5, -5, -1], [5, -5, -1],    [5, 5, -1], 
                        [-5, -5, -1], [5, 5, -1],     [-5, 5, -1] ]
        colors      = [ [1, 1, 0.2, 1], [1, 1, 0.2, 1], [1, 0, 0.2, .5],
                        [1, 1, 0.2, 1], [1, 0, 0.2, .5], [1, 0, 0.2, .5]]
        normals     = [ [1, 1, 1], [1, 1, 1], [1, 1, 1],
                        [1, 1, 1], [1, 1, 1], [1, 1, 1]]
        return [np.array(vertices), np.array(colors), np.array(normals)]

