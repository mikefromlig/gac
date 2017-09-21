#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import math
import time
import libs.viewpoint   as vp

class camera():
    def __init__(self, position, look_at, view_angle, ratio):
        
        #projection params
        self.position   = position
        self.look_at    = look_at
        self.up         = [0,1,0]
        self.v_angle    = view_angle
        self.ratio      = ratio
        self.near       = .01
        self.far        = 1000.
        
        self.m_projection = None
        self.m_modelview = None
        
        #wiggling params
        self.wiggle             = False
        self.wiggle_pivot       = self.look_at
        self.wiggle_position    = self.position
        self.wiggle_look_at     = self.look_at
        self.wiggle_speed       = 4             # arc per seconds
        self.wiggle_arc         = math.pi/10    # wiggle amplitude
        self.wiggle_time        = time.time()
        self.wiggle_angle       = 0
        
        
    def compute_perspective(self, ratio):
        self.ratio = ratio
        self.m_projection= vp.perspective(self.v_angle, self.ratio, self.near, self.far) 
        
        
    def compute_modelview(self):
        self.m_modelview = vp.look_at(self.wiggle_position, self.wiggle_look_at, self.up)
        
        
    def wiggle_next(self):
        t = time.time()
        dt = self.wiggle_time - t
        
        self.wiggle_angle = (math.sin(dt*2*self.wiggle_speed))*self.wiggle_arc/2.0
        angle = self.wiggle_angle
        
        self.wiggle_position = vp.rotate(self.position, self.up, angle, self.wiggle_pivot)
        self.wiggle_look_at = vp.rotate(self.look_at, self.up, angle, self.wiggle_pivot)
        self.compute_modelview()
    