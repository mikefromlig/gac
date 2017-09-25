#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import sys
import numpy as np


class pivot_point:
    def __init__(self):
        self.sh             = None
        self.vbos           = None
        self.model          = None
        self.display        = True
        self.displacement   = np.identity(4)
        
        self.model = self.make_model()
        
    def make_model(self):
        scale = [0.02, 100, 0.02]
        vertices    = [ [-1, -1, 1], [1, -1, 1],    [1, 1, 1], 
                        [-1, -1, 1], [1, 1, 1],    [-1, 1, 1],
                        
                        [1, -1, 1], [1, -1, -1],    [1, 1, -1], 
                        [1, -1, 1], [1, 1, -1],    [1, 1, 1],
                        
                        [-1, -1, -1], [-1, -1, 1],    [-1, 1, 1], 
                        [-1, -1, -1], [-1, 1, 1],    [-1, 1, -1],
                        
                        [-1, 1, -1], [-1, 1, 1],    [1, 1, 1], 
                        [-1, 1, -1], [1, 1, 1],    [1, 1, -1],

                        [-1, -1, -1], [1, -1, -1],    [1, -1, 1], 
                        [-1, -1, -1], [1, -1, 1],    [-1, -1, 1]
                        ]
        colors = []
        color = [1,0,0,.4]
        for i in range(6*5):
            colors.append(color)
                        
        normals     = [ [0, 0, 1], [0, 0, 1], [0, 0, 1],
                        [0, 0, 1], [0, 0, 1], [0, 0, 1],
                        [1, 0, 0], [1, 0, 0], [1, 0, 0],
                        [1, 0, 0], [1, 0, 0], [1, 0, 0],
                        [-1, 0, 0], [-1, 0, 0], [-1, 0, 0],
                        [-1, 0, 0], [-1, 0, 0], [-1, 0, 0],
                        [0, 1, 0], [0, 1, 0], [0, 1, 0],
                        [0, 1, 0], [0, 1, 0], [0, 1, 0],
                        [0, -1, 0], [0, -1, 0], [0, -1, 0],
                        [0, -1, 0], [0, -1, 0], [0, -1, 0]]

        
        return [np.array(vertices)*scale, np.array(colors), np.array(normals)]
    