#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 05/Oct/2017

import numpy            as np
import libs.iso_circle  as iso
import libs.distractor  as dis

class expe_data():
    def __init__(self, nb_target_per_circle = 13, amplitude = 8):
        self.user_name      = "testman"
        self.technique      = "none"
        self.ids            = np.array([[3, .6], [4, .3], [5, .2], [6, .1]])
        self.nb_trials      = 10
        self.circles        = []
        self.models         = []
        self.nb_t_p_circ    = nb_target_per_circle
        self.amplitude      = 8
        self.current_index  = 0
        self.current_circle = None
        self.current_model  = None
        
        for id in self.ids:
            self.circles.append(iso.iso_circle(self.nb_t_p_circ, self.amplitude, id[0], id[1]))
            self.models.append(dis.make_distractor(self.circles[-1].ID, self.circles[-1].amplitude, self.circles[-1].rho, self.circles[-1].width))
        
        arr = np.arange(len(self.ids)).reshape((len(self.ids), 1))
        self.ids = np.concatenate((self.ids, arr), axis=1)
        
        self.shuffle_trials()
        
        self.current_circle = self.circles[int(self.conf[0][2])]
        self.current_model  = self.models[int(self.conf[0][2])]
        
    def shuffle_trials(self):
        self.conf = np.repeat(self.ids, self.nb_trials, axis=0)
        np.random.shuffle(self.conf)
        
    def save_current_conf(self):
        np.save("ids", self.conf[self.current_index:])
        
    def reload_conf(self):
        self.confs = np.load("ids.npy")
        
    def next(self):
        self.current_index += 1
        if self.current_index == len(self.conf):
            return False
        self.current_circle = self.circles[int(self.conf[self.current_index][2])]
        self.current_model  = self.models[int(self.conf[self.current_index][2])]
        
        self.save_current_conf()
        return True
        
    def print_current_conf(self):
        print("expe conf", self.current_index, ":", *self.conf[self.current_index])

