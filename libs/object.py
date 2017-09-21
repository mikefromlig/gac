#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import sys
import math
import numpy as np

class object:
    def __init__(self, file=None):
        self.sh         = None
        self.vbos       = None
        self.model      = None
        self.display    = True
        
        if not file:
            self.model = self.make_distractor()
        else:
            print("Obj parser not implemented yet !!!")
            sys.exit()
        
    def make_distractor(self):
        vertices    = [[0, 0, 0], [3, 0, 0], [0, 3, 0]]
        colors      = [[1, 1, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1]]
        return [np.array(vertices), np.array(colors)]
    