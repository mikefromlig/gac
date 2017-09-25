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
import libs.iso_circle  as ic
import libs.object      as o
import libs.pdp         as pdp
from libs.camera import *

################################################################################
# GLOBALS

## interaction
window  = {'w': 800, 'h': 600}
mouse   = {'x': -1, 'y': -1}

## iso_circle
iso_circle = ic.iso_circle(9, 8, 4, .3) # nb targets, amplitude, ID
iso_circle.make_circle()

## distractor
object = o.object(_iso_circle = iso_circle)

## camera
cam = camera([0, 0, 15], [0, 0, 0], [0, 1, 0], 45.0, window['w']/window['h'])
cam.wiggle = True


pdp = pdp.pivot_point()
pdp.display = False

################################################################################
# INIT & COMPUTATION FUNCS


def mouse_intersection(mouse_x, mouse_y, camera, win_w, win_h):
    
    winZ = glReadPixels( mouse_x, win_h - mouse_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT);
    if winZ[0][0] > 0.99999999:
        return [0, 0, 0]
    
    inv = np.linalg.inv(np.dot(camera.m_projection, camera.m_modelview))
    res = inv.dot([     2*(mouse_x)/win_w -1,
                        2*(win_h - mouse_y)/win_h -1,
                        2*winZ -1,
                        1   ])
    return (res/res[3])[:3]


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
    # iso circle shader
    iso_circle.vbos     = glGenBuffers(2)
    iso_circle_sh_attr  = [0, 1]
    
    glBindBuffer(GL_ARRAY_BUFFER, iso_circle.vbos[0])
    glBufferData(GL_ARRAY_BUFFER, iso_circle.model[0].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(iso_circle_sh_attr[0], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(iso_circle_sh_attr[0])
    
    glBindBuffer(GL_ARRAY_BUFFER, iso_circle.vbos[1])
    glBufferData(GL_ARRAY_BUFFER, iso_circle.model[1].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(iso_circle_sh_attr[1], 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(iso_circle_sh_attr[1])
    
    print('\tIso circle shader...', end='')
    iso_circle.sh = sh.create('shaders/iso_circle_vert.vert',None,'shaders/iso_circle_frag.vert', iso_circle_sh_attr, ['in_vertex', 'in_color'])
    if not iso_circle.sh:
        exit(1)
    print('\tOk')
    
    
    ##########################
    # object shader
    object.vbos     = glGenBuffers(3)
    object_sh_attr  = [2, 3, 4]
    
    #vertices
    glBindBuffer(GL_ARRAY_BUFFER, object.vbos[0])
    glBufferData(GL_ARRAY_BUFFER, object.model[0].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(object_sh_attr[0], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(object_sh_attr[0])
    
    #colors
    glBindBuffer(GL_ARRAY_BUFFER, object.vbos[1])
    glBufferData(GL_ARRAY_BUFFER, object.model[1].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(object_sh_attr[1], 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(object_sh_attr[1])
    
    #normals
    glBindBuffer(GL_ARRAY_BUFFER, object.vbos[2])
    glBufferData(GL_ARRAY_BUFFER, object.model[2].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(object_sh_attr[2], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(object_sh_attr[2])
    
    print('\tObject shader...', end='')
    object.sh = sh.create('shaders/object_vert.vert',None,'shaders/object_frag.vert', object_sh_attr, ['in_vertex', 'in_color', 'in_normal'])
    if not object.sh:
        exit(1)
    print('\tOk')
    
    
    ##########################
    # pdp shader
    pdp.vbos     = glGenBuffers(3)
    pdp_sh_attr  = [5, 6, 7]
    
    #vertices
    glBindBuffer(GL_ARRAY_BUFFER, pdp.vbos[0])
    glBufferData(GL_ARRAY_BUFFER, pdp.model[0].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(pdp_sh_attr[0], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(pdp_sh_attr[0])
    
    #colors
    glBindBuffer(GL_ARRAY_BUFFER, pdp.vbos[1])
    glBufferData(GL_ARRAY_BUFFER, pdp.model[1].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(pdp_sh_attr[1], 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(pdp_sh_attr[1])
    
    #normals
    glBindBuffer(GL_ARRAY_BUFFER, pdp.vbos[2])
    glBufferData(GL_ARRAY_BUFFER, pdp.model[2].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(pdp_sh_attr[2], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(pdp_sh_attr[2])
    
    print('\tPdp shader...', end='')
    pdp.sh = sh.create('shaders/pdp_vert.vert',None,'shaders/pdp_frag.vert', pdp_sh_attr, ['in_vertex', 'in_color', 'in_normal'])
    if not pdp.sh:
        exit(1)
    print('\tOk')
    
    ##########################
    # init projections
    cam.compute_modelview()
    cam.compute_perspective(window['w']/window['h'])
    
    glUseProgram(iso_circle.sh)
    projection(iso_circle.sh, cam.m_projection, cam.m_modelview)
    
    glUseProgram(pdp.sh)
    projection(pdp.sh, cam.m_projection, cam.m_modelview)
    
    unif_d = glGetUniformLocation(pdp.sh, "displacement")
    glUniformMatrix4fv(unif_d, 1, False, pdp.displacement)
    
    glUseProgram(object.sh)
    projection(object.sh, cam.m_projection, cam.m_modelview)
    
    unif_d = glGetUniformLocation(object.sh, "displacement")
    glUniformMatrix4fv(unif_d, 1, False, object.displacement)


def init():
    print("\nInit")
    init_OGL()
    init_shaders()


################################################################################
# DISPLAY FUNCS


'''
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
'''

def display():
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    if object.display and iso_circle.current > 0:
        glUseProgram(object.sh)
        
        glBindBuffer(GL_ARRAY_BUFFER, object.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, object.model[0].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, object.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, object.model[1].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, object.vbos[2])
        glBufferData(GL_ARRAY_BUFFER, object.model[2].astype('float32'), GL_DYNAMIC_DRAW)
        
        glDrawArrays(GL_TRIANGLES, 0, len(object.model[0]))
        
    if iso_circle.display:
        glUseProgram(iso_circle.sh)
        
        glBindBuffer(GL_ARRAY_BUFFER, iso_circle.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, iso_circle.model[0].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, iso_circle.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, iso_circle.model[1].astype('float32'), GL_DYNAMIC_DRAW)
        
        glDrawArrays(GL_TRIANGLES, 0, len(iso_circle.model[0]))
        
    if mouse_over_window():
        cam.wiggle_pivot = mouse_intersection(mouse['x'], mouse['y'], cam, window['w'], window['h'])
    
    if iso_circle.display and iso_circle.display_all:
        glDisable(GL_DEPTH_TEST)
        glUseProgram(iso_circle.sh)
        
        glBindBuffer(GL_ARRAY_BUFFER, iso_circle.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, iso_circle.model[0].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, iso_circle.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, iso_circle.model[1].astype('float32'), GL_DYNAMIC_DRAW)
        
        glDrawArrays(GL_TRIANGLES, 0, len(iso_circle.model[0]))
        glEnable(GL_DEPTH_TEST)
    
    if pdp.display:
        glUseProgram(pdp.sh)
        
        glBindBuffer(GL_ARRAY_BUFFER, pdp.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, pdp.model[0].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, pdp.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, pdp.model[1].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, pdp.vbos[2])
        glBufferData(GL_ARRAY_BUFFER, pdp.model[2].astype('float32'), GL_DYNAMIC_DRAW)
        
        glDrawArrays(GL_TRIANGLES, 0, len(pdp.model[0]))
    #glEnable(GL_DEPTH_TEST)
    
    glutSwapBuffers()


################################################################################
# INTERACTION FUNCS

def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit()
    elif key == b'f':
        glutFullScreen()
    elif key == b'w':
        cam.wiggle = not cam.wiggle
    elif key == b't':
        iso_circle.display = not iso_circle.display
    elif key == b'a':
        iso_circle.display_all = not iso_circle.display_all
        iso_circle.make_circle()
    elif key == b'o':
        object.display = not object.display
    elif key == b'p':
        pdp.display = not pdp.display
    else:
        print(key)
    
    glutPostRedisplay()


def clicks(button, state, x, y):
    
    mouse['x'] = x
    mouse['y'] = y
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if iso_circle.is_current_clicked([x, window['h']-y], cam.m_projection, cam.m_modelview, window['w'], window['h']):
                
                if iso_circle.current >= 0:
                    p = iso_circle.positions[iso_circle.current]
                    object.displacement = np.identity(4)
                    object.displacement[3][0] = p[0]
                    object.displacement[3][1] = p[1]
                    glUseProgram(object.sh)
                    unif_d = glGetUniformLocation(object.sh, "displacement")
                    glUniformMatrix4fv(unif_d, 1, False, object.displacement)
                
                iso_circle.next()
                iso_circle.make_circle()
    
    glutPostRedisplay()


def mouse_passive(x, y):
    mouse['x'] = x
    mouse['y'] = y
    
    glutPostRedisplay()


def mouse_over_window():
    if  mouse['x'] >= 0 and \
        mouse['x'] <= window['w'] and \
        mouse['y'] >= 0 and \
        mouse['y'] <= window['h'] :
        return True
    else:
        return False


def idle():
    window['w'] = glutGet(GLUT_WINDOW_WIDTH)
    window['h'] = glutGet(GLUT_WINDOW_HEIGHT)
    
    #projection update (in case the window is reshaped)
    cam.compute_perspective(window['w']/window['h'])
    
    #wiggling rotation
    if cam.wiggle:
        cam.wiggle_next()
    
    glUseProgram(iso_circle.sh)
    projection(iso_circle.sh, cam.m_projection, cam.m_modelview)
    
    glUseProgram(object.sh)
    projection(object.sh, cam.m_projection, cam.m_modelview)
    
    glUseProgram(pdp.sh)
    projection(pdp.sh, cam.m_projection, cam.m_modelview)
    
    pdp.displacement = np.identity(4)
    pdp.displacement[3][0] = cam.wiggle_pivot[0]
    pdp.displacement[3][1] = cam.wiggle_pivot[1]
    pdp.displacement[3][2] = cam.wiggle_pivot[2]
    glUseProgram(pdp.sh)
    unif_d = glGetUniformLocation(pdp.sh, "displacement")
    glUniformMatrix4fv(unif_d, 1, False, pdp.displacement)
    
    glutPostRedisplay()


################################################################################
# SANDBOX


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


## Display commands
print()
print("Commands:")
print("\t'esc': exit")
print("\t'f': fullscreen")
print("\t'w': start/stop wiggle")
print("\t'p': display/hide pivot point")
print("\t'o': display/hide object")
print("\t'a': display all/one target")

glutMainLoop()