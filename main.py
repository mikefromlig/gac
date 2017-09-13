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


################################################################################
# INIT FUNCS


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
    targets_vbos     = [glGenBuffers(1)]
    targets_sh_attr  = [0]
    
    targets_model = np.array([])
    glBindBuffer(GL_ARRAY_BUFFER, targets_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, targets_model.astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(targets_sh_attr[0], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(targets_sh_attr[0])
    
    print('\tTargets feedback shader...', end='')
    targets_sh = sh.create('shaders/targets_vert.vert',None,'shaders/targets_frag.vert', targets_sh_attr, [])
    if not targets_sh:
        exit(1)
    print('\tOk')
    
    ##########################
    # init projections
    m_persp_modelview   = np.identity(4)
    m_persp_modelview[2][3] = -7.5
    m_persp_projection  = vp.perspective(45.0, window['w']/window['h'], 0.01, 10000.)
    
    glUseProgram(targets_sh)
    projection(targets_sh, m_persp_projection, m_persp_modelview)
    
    #targets_model = cursor_feedback(list(mouse.values()))
    targets_model = iso_circle(5, 1, 9)


def init():
    init_OGL()
    init_shaders()

################################################################################
# DISPLAY FUNCS

def circle(p, r, nb_arcs):
    return np.array([])


def iso_circle(D, W, nb_targets):
    
    targets = []
    arc = 2*math.pi/nb_targets
    for i in range(nb_targets):
        targets.extend(circle([0,0,0], W/2.0, 20))
    
    return np.array(targets)


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
    glBufferData(GL_ARRAY_BUFFER, targets_model.astype('float32'), GL_DYNAMIC_DRAW)
    glDrawArrays(GL_TRIANGLES, 0, len(targets_model))
    
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
glutPassiveMotionFunc(mouse_passive)
glutIdleFunc(idle)
glutMainLoop()