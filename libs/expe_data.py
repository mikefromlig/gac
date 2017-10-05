#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 05/Oct/2017

import numpy as np

class expe_data():
    def __init__(self):
        self.user_name  = "testman"
        self.technique  = "none"
        self.ids        = np.array([[3, .6], [4, .3], [5, .2], [6, .1]])
        self.nb_trials  = 10
        self.current    = 0
        
        self.shuffle_trials()
        
    def shuffle_trials(self):
        self.conf = np.repeat(self.ids, self.nb_trials, axis=0)
        np.random.shuffle(self.conf)
        
    def save_current_conf(self):
        np.save("ids", self.conf[self.current:])
        
    def reload_conf(self):
        self.confs = np.load("ids.npy")
        
    def next(self):
        self.current += 1
        if self.current == len(self.conf):
            return False
        
        self.save_current_conf()
        return True
        
    def print_current_conf(self):
        print("\nexpe conf", self.current, ":", *self.conf[self.current])

