#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA, LIG/CNRS - 25/Oct/2017

import os

header = None
lines = []
for f_name in os.listdir('.'):
    if f_name[-4:] == '.csv' and not f_name == 'all.csv':
        f = open(f_name, 'r')
        
        #user_name
        user = f_name.split('_')[0]
        
        #reading first line
        header = f.readline()
        for line in f.readlines():
            lines.append(user+','+line)
        f.close()

f = open('all.csv', 'w')
f.write('user,'+header)
for line in lines:
    f.write(line)
f.close()

print('user,'+header)