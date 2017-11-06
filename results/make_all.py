#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA, LIG/CNRS - 25/Oct/2017

import os
import numpy

header = None
lines = []
for f_name in os.listdir('.'):
    if f_name[-4:] == '.csv' and not f_name in ['all.csv', 'aggre_by_angle.csv', 'aggre.csv']:
        f = open(f_name, 'r')
        
        #user_name
        user = f_name.split('_')[0]
        
        #reading first line
        header = ['user']
        header.extend(f.readline().split(','))
        header[-1] = header[-1].rstrip()
        
        #other lines
        for line in f.readlines():
            lines.append([user])
            lines[-1].extend(line.split(','))
            lines[-1][4] = int(float(lines[-1][4]))
            lines[-1][-1] = lines[-1][-1].rstrip()
            
            #Bug correction
            if lines[-1][4] == 307: lines[-1][4] = 171
            if lines[-1][4] == 35:  lines[-1][4] = 335
            if lines[-1][4] == 339: lines[-1][4] = 139
            if lines[-1][4] == 6:   lines[-1][4] = 302
            if lines[-1][4] == 173: lines[-1][4] = 106
            if lines[-1][4] == 200: lines[-1][4] = 270
            if lines[-1][4] == 144: lines[-1][4] = 73
            if lines[-1][4] == 232: lines[-1][4] = 237
            if lines[-1][4] == 109: lines[-1][4] = 40
            if lines[-1][4] == 270: lines[-1][4] = 204
        f.close()

#aggregations
aggre_a = {}
for line in lines[:]:
    k = line[0]+','+line[1]+','+line[2]+','+str(line[4])
    if k in aggre_a.keys():
        aggre_a[k][7].append(float(line[7]))
        aggre_a[k][8]     += float(line[8])
        aggre_a[k][9]     += float(line[9])
        aggre_a[k][10]    += float(line[10])
        aggre_a[k][11]    += 1
    else:
        res = line[:]
        res[5] = float(line[5])
        res[6] = float(line[6])
        res[7] = [float(line[7])]
        res[8] = float(line[8])
        res[9] = float(line[9])
        res[10] = float(line[10])
        res.append(0)
        
        aggre_a[k] = res[:]

aggre   = {}
for line in lines[:]:
    k = line[0]+','+line[1]+','+line[2]
    if k in aggre.keys():
        aggre[k][7].append(float(line[7]))
        aggre[k][8]     += float(line[8])
        aggre[k][9]     += float(line[9])
        aggre[k][10]    += float(line[10])
        aggre[k][11]    += 1
    else:
        res = line[:]
        res[5] = float(line[5])
        res[6] = float(line[6])
        res[7] = [float(line[7])]
        res[8] = float(line[8])
        res[9] = float(line[9])
        res[10] = float(line[10])
        res.append(0)
        
        aggre[k] = res[:]


for k in aggre_a:
    aggre_a[k][7]     = 4.1333*numpy.std(aggre_a[k][7])
    aggre_a[k][8]     /= aggre_a[k][11]
    aggre_a[k][9]     /= aggre_a[k][11]
    aggre_a[k][10]    /= aggre_a[k][11]
    aggre_a[k].pop()


for k in aggre:
    aggre[k][7]     = 4.1333*numpy.std(aggre[k][7])
    aggre[k][8]     /= aggre[k][11]
    aggre[k][9]     /= aggre[k][11]
    aggre[k][10]    /= aggre[k][11]
    aggre[k].pop()

import csv
with open('all.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(header)
    for line in lines:
        spamwriter.writerow(line)

with open('aggre_by_angle.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(header)
    for k in aggre_a.keys():
        spamwriter.writerow(aggre_a[k])

with open('aggre.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    header.pop(4)
    spamwriter.writerow(header)
    for k in aggre.keys():
        aggre[k].pop(4)
        spamwriter.writerow(aggre[k])