#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import math
import numpy as np

class object:
    def __init__(self):
        self.sh         = None
        self.vbos       = None
        self.model      = None
        self.display    = True
        
        self.make_model()
        
    def make_model(self):
        vertices    = [[0, 0, 0], [3, 0, 0], [0, 3, 0]]
        colors      = [[1, 1, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1]]
        self.model = [np.array(vertices), np.array(colors)]
    