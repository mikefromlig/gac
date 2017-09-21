#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 21/Sept/2017

import libs.viewpoint   as vp

class camera():
    def __init__(self, position, look_at, view_angle, ratio):
        self.position = position
        self.look_at = look_at
        self.v_angle = view_angle
        self.ratio = ratio
        self.near = 0.001
        self.far = 100000.
        
        self.m_projection = None
        self.m_modelview = None

    def compute_perspective(self, ratio):
        self.ratio = ratio
        self.m_projection= vp.perspective(self.v_angle, self.ratio, self.near, self.far)            