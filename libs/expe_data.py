#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 05/Oct/2017

import math
import numpy            as np
import libs.iso_circle  as iso
import libs.distractor  as dis


def distance(a, b):
    r = 0
    for i in  range(len(a)):
        r += (a[i]-b[i])*(a[i]-b[i])
    return math.sqrt(r)


def vector(a, b):
    v = []
    for i in range(len(a)):
        v.append(b[i] - a[i])
    return v


def norm(v):
    n = 0
    for i in v:
        n += i*i
    return math.sqrt(n)


def normalized(v):
    res = v[:]
    n = norm(res)
    for i in range(len(res)):
        res[i] /= n
    return res, n


def dot(u, v):
    d = 0
    for i in range(len(u)):
        d += u[i]*v[i]
    return d


def cross(v1,v2):
    return [v1[1]*v2[2]-v1[2]*v2[1],
            v1[2]*v2[0]-v1[0]*v2[2],
            v1[0]*v2[1]-v1[1]*v2[0]]


class expe_data():
    def __init__(self, nb_target_per_circle = 13, diameter = 8, win_w = 800, win_h = 600):
        self.user_name      = "testman"
        self.technique      = "none"
        self.ids            = np.array([[3, .6], [4, .3], [5, .2], [6, .1]])
        self.nb_trials      = 10
        self.trials         = []
        self.circles        = []
        self.models         = []
        self.time           = 0
        self.mouse          = [0, 0]
        self.nb_t_p_circ    = nb_target_per_circle
        self.diameter      = diameter
        self.current_index  = 0
        self.missed         = 0
        
        #camera info
        self.cam            = None
        self.window_w       = win_w
        self.window_h       = win_h
        
        
        for id in self.ids:
            self.circles.append(iso.iso_circle(self.nb_t_p_circ, self.diameter, id[0], id[1]))
            self.models.append(dis.make_distractor(self.circles[-1].ID, self.circles[-1].amplitude, self.circles[-1].rho, self.circles[-1].width))
        
        arr = np.arange(len(self.ids)).reshape((len(self.ids), 1))
        self.ids = np.concatenate((self.ids, arr), axis=1)
        
        self.shuffle_trials()
        
        self.current_circle = self.circles[int(self.confs[0][2])]
        self.current_model  = self.models[int(self.confs[0][2])]
        
    def project(self, p):
        n_p = self.cam.i_m_projection.dot(self.cam.i_m_modelview.dot(np.array(p)))
        n_p = n_p/n_p[3]
        n_p = n_p/n_p[2]
        return [self.window_w*(n_p[0]+1)/2.0, self.window_h*(n_p[1]+1)/2.0]
    
    def shuffle_trials(self):
        self.confs = np.repeat(self.ids, self.nb_trials, axis=0)
        np.random.shuffle(self.confs)
    
    def save_current_conf(self):
        np.save("ids", self.confs[self.current_index:])
    
    def reload_conf(self):
        self.confs = np.load("ids.npy")
    
    def next(self):
        self.current_index += 1
        if self.current_index == len(self.confs):
            return False
        self.current_circle = self.circles[int(self.confs[self.current_index][2])]
        self.current_model  = self.models[int(self.confs[self.current_index][2])]
        
        self.save_current_conf()
        return True
    
    def print_current_conf(self):
        print("expe conf", self.current_index, ":", *self.confs[self.current_index])
    
    def new_trial(self, t, m):
        prev_pos = self.current_circle.positions[self.current_circle.current_target -1]
        new_pos = self.current_circle.positions[self.current_circle.current_target]
        sil_pos = new_pos[:]
        sil_pos[0] += self.current_circle.width/2.0 #outline point along X axis
        
        p_prev_pos  = self.project(prev_pos)
        p_new_pos   = self.project(new_pos)
        p_sil_pos   = self.project(sil_pos)
        
        self.trials.append({'id':               self.confs[self.current_index][0],
                            'rho':              self.confs[self.current_index][1],
                            'width':            distance(p_sil_pos, p_new_pos)*2,
                            'mt':               t - self.time, 
                            'prev_click':       self.mouse,
                            'new_click':        m, 
                            'prev_target_pos':  p_prev_pos, 
                            'new_target_pos':   p_new_pos,
                            'error':            self.missed
                            })
        self.save_trials()
    
    def save_trials(self):
        f = open('results/'+self.user_name+'_'+self.technique+'.csv', 'w')
        f.write("id,rho,angle,w,a,we,ae,mt,error\n")
        
        for t in self.trials:
            travelled_dist = distance(t['prev_click'], t['new_click'])
            targets_dist = distance(t['prev_target_pos'], t['new_target_pos'])
            v_up = [1,0]
            v_targets, n = normalized(vector(t['prev_target_pos'], t['new_target_pos']))
            angle = math.acos(dot(v_up, v_targets))*180/math.pi
            
            v_we, n_v_we = normalized(vector(t['new_target_pos'], t['new_click']))
            we = math.fabs(n_v_we*dot(v_we, v_targets))
            
            v_clicks, n_v_clicks = normalized(vector(t['prev_click'],t['new_click']))
            ae = math.fabs(n_v_clicks*dot(v_clicks, v_targets))
            
            if cross([v_up[0], v_up[1], 0], [v_targets[0], v_targets[1], 0])[2] < 0:
                angle = angle + 180
            
            f.write(str(t['id'])                    +','+ #id
                    str(t['rho'])                   +','+ #rho
                    str(angle)                      +','+ #angle
                    str(t['width'])                 +','+ #w
                    str(targets_dist)               +','+ #a
                    str(we)                         +','+ #we
                    str(ae)                         +','+ #ae
                    str(t['mt'])                    +','+ #mt
                    str(t['error'])                 +'\n' #error \
                    )
        f.close()

