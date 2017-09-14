#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 11/09/2017

###### GLOBAL LIBS
import sys
import numpy as np
import math
try:
    from OpenGL.GL      import *
    from OpenGL.GLU     import *
    from OpenGL.GLUT    import *
    from OpenGL.GL      import shaders
except:
    print ('''ERROR: PyOpenGL not installed properly.''')


###### LOCAL LIBS
import libs.shader      as sh
import libs.viewpoint    as vp

################################################################################
# GLOBALS

window  = {'w': 800, 'h': 600}
mouse   = {'x': 0, 'y': 0}

## shaders
targets_sh = None
targets_current = 0
targets_radius = .3
targets_amplitude = 3
targets_nb = 9
targets_positions = []


################################################################################
# INIT & COMPUTATION FUNCS

def distance(a, b):
    r = 0
    for i in range(len(a)):
        r += (a[i]-b[i])*(a[i]-b[i])
    return math.sqrt(r)


def next_target():
    return (targets_current + int(targets_nb/2)) % targets_nb

#m: mouse position ; r: target radius
def is_target_clicked(m, i):
    
    #target_center
    pc = m_persp_projection.dot(m_persp_modelview.dot(np.array(targets_positions[i])))
    pc = pc/pc[3]
    pc = pc/pc[2]
    pc = [window['w']*(pc[0]+1)/2.0, window['h']*(pc[1]+1)/2.0]
    
    #target_edge
    edge = np.array(targets_positions[i]) + np.array([1, 0, 0, 0])*targets_radius
    pe = m_persp_projection.dot(m_persp_modelview.dot(edge))
    pe = pe/pe[3]
    pe = pe/pe[2]
    pe = [window['w']*(pe[0]+1)/2.0, window['h']*(pe[1]+1)/2.0]
    
    dtm = distance(pc, m)
    r   = distance(pe, pc)
    
    if dtm <= r:
        return 1
    else:
        return 0

def projection(sh, matp, matm):
    
    #projection * view * model
    unif_p = glGetUniformLocation(sh, "projection_mat")
    unif_m = glGetUniformLocation(sh, "modelview_mat")
    
    glUniformMatrix4fv(unif_p, 1, False, matp.T)
    glUniformMatrix4fv(unif_m, 1, False, matm.T)


def init_OGL():
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glClearColor(1,1,1,1)


def init_shaders():
    global targets_vbos, targets_sh, targets_model
    global m_persp_projection
    global m_persp_modelview
    
    ##########################
    # general vertex array object
    print('\tGenerating vao...', end='')
    try:
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        print('\t\tOk')
    except ValueError:
        print()
        print()
        print(ValueError)
        print()
        sys.exit()
    
    ##########################
    # techniques shader (visual feedback)
    targets_vbos     = glGenBuffers(2)
    targets_sh_attr  = [0, 1]
    
    targets_model = [np.array([]), np.array([])]
    glBindBuffer(GL_ARRAY_BUFFER, targets_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, targets_model[0].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(targets_sh_attr[0], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(targets_sh_attr[0])
    
    glBindBuffer(GL_ARRAY_BUFFER, targets_vbos[1])
    glBufferData(GL_ARRAY_BUFFER, targets_model[1].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(targets_sh_attr[1], 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(targets_sh_attr[1])
    
    print('\tTargets feedback shader...', end='')
    targets_sh = sh.create('shaders/targets_vert.vert',None,'shaders/targets_frag.vert', targets_sh_attr, ['in_vertex', 'in_color'])
    if not targets_sh:
        exit(1)
    print('\tOk')
    
    ##########################
    # init projections
    m_persp_modelview   = np.identity(4)
    m_persp_modelview[2][3] = -10
    m_persp_projection  = vp.perspective(45.0, window['w']/window['h'], 0.01, 10000.)
    
    glUseProgram(targets_sh)
    projection(targets_sh, m_persp_projection, m_persp_modelview)
    
    targets_model = iso_circle(targets_amplitude, targets_radius*2, targets_nb, targets_current)


def init():
    init_OGL()
    init_shaders()


################################################################################
# DISPLAY FUNCS

def circle(p, r, nb_arcs, color):
    angle = 2*math.pi/nb_arcs
    arr, col = [], []
    for i in range(nb_arcs):
        x1 = math.cos(i*angle)*r
        y1 = math.sin(i*angle)*r
        x2 = math.cos((i+1)*angle)*r
        y2 = math.sin((i+1)*angle)*r
        
        arr.append(np.array([0,    0,  0])+p)
        arr.append(np.array([x1,   y1, 0])+p)
        arr.append(np.array([x2,   y2, 0])+p)
        col.append(color)
        col.append(color)
        col.append(color)
    return np.array(arr), np.array(col)


def iso_circle(D, W, nb_targets, hi_id):
    
    global targets_positions
    targets = []
    colors = []
    angle = 2*math.pi/nb_targets
    
    targets_positions = []
    for i in range(nb_targets):
        x = math.cos(i*angle)*D
        y = math.sin(i*angle)*D
        color = [1, 0, 0, .3]
        if i == hi_id:
            color = [0, 1, 0, 1]
        t, c = circle([x, y, 0], W/2.0, 20, color)
        targets.extend(t)
        colors.extend(c)
        targets_positions.append([x, y, 0, 1])
        
    return [np.array(targets), np.array(colors)]


def cursor_feedback(p):
    left    = np.array([1,0])
    up      = np.array([0,1])
    r = 5
    arr = []
    
    nb_steps = 20
    step = 2*math.pi/nb_steps
    for i in range(nb_steps):
        arr.append(p)
        arr.append(p + r*math.cos((i+1)*step)*left + r*math.sin((i+1)*step)*up)
        arr.append(p + r*math.cos(i*step)*left + r*math.sin(i*step)*up)
    
    z = np.zeros((len(arr),1), dtype='float32')
    return np.append(arr, z, axis=1)


def display():
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    #########################
    # display targets
    glUseProgram(targets_sh)
    glBindBuffer(GL_ARRAY_BUFFER, targets_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, targets_model[0].astype('float32'), GL_DYNAMIC_DRAW)
    
    glBindBuffer(GL_ARRAY_BUFFER, targets_vbos[1])
    glBufferData(GL_ARRAY_BUFFER, targets_model[1].astype('float32'), GL_DYNAMIC_DRAW)

    glDrawArrays(GL_TRIANGLES, 0, len(targets_model[0]))
    
    glutSwapBuffers()


################################################################################
# INTERACTION FUNCS

def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit()
    elif key == b'f':
        glutFullScreen()
    
    else:
        print(key)


def clicks(button, state, x, y):
    
    global targets_current, targets_model
    
    mouse['x'] = x
    mouse['y'] = y
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if is_target_clicked([x, window['h']-y], targets_current):
                targets_current = next_target()
                targets_model = iso_circle(targets_amplitude, targets_radius*2, targets_nb, targets_current)
    
    glutPostRedisplay()


def mouse_passive(x, y):
    mouse['x'] = x
    mouse['y'] = y
    
    glutPostRedisplay()


def idle():
    window['w'] = glutGet(GLUT_WINDOW_WIDTH)
    window['h'] = glutGet(GLUT_WINDOW_HEIGHT)


################################################################################
# MAIN

glutInit(sys.argv)
glutInitDisplayString('double rgba samples=8 depth core')
glutInitWindowSize (window['w'], window['h'])
glutCreateWindow ('Selecting Boids (geometry shader)')

init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(clicks)
glutPassiveMotionFunc(mouse_passive)
glutIdleFunc(idle)
glutMainLoop()