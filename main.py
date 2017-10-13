#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 11/09/2017

###### GLOBAL LIBS
import sys
import numpy    as np
import math
import platform as pl

try:
    from OpenGL.GL      import *
    from OpenGL.GLU     import *
    from OpenGL.GLUT    import *
    from OpenGL.GL      import shaders
except:
    print ('''ERROR: PyOpenGL not installed properly.''')


###### LOCAL LIBS
from    libs.camera     import *
from    libs.expe_data  import *
import  libs.distractor as dis
import  libs.shader     as sh
import  libs.iso_circle as ic
import  libs.object     as o
import  libs.pdp        as pdp
import  libs.tobii     as tobii

################################################################################
# GLOBALS

## interaction
window_w, window_h = 800, 600
mouse   = [-1, -1]
eye     = [-1, -1]

## expe info
expe = expe_data(3, 8)

## targets
targets = o.object()
targets.model = expe.current_circle.model

## distractor
object = o.object()
object.model = expe.current_model


## eye
eye_disc = o.object()

## camera
cam = camera([0, 0, 15], [0, 0, 0], [0, 1, 0], 45.0, window_w/window_h)
cam.wiggle = True

## pivot point display
pdp = pdp.pivot_point()
pdp.display = False

tob = tobii.tobii("129.88.65.158", 8888)        #tobii udp connection

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
        print('\tOk')
    except ValueError:
        print()
        print()
        print(ValueError)
        print()
        sys.exit()
    
    ##########################
    # iso circle shader
    targets.vbos     = glGenBuffers(2)
    targets_sh_attr  = [0, 1]
    
    glBindBuffer(GL_ARRAY_BUFFER, targets.vbos[0])
    glBufferData(GL_ARRAY_BUFFER, targets.model[0].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(targets_sh_attr[0], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(targets_sh_attr[0])
    
    glBindBuffer(GL_ARRAY_BUFFER, targets.vbos[1])
    glBufferData(GL_ARRAY_BUFFER, targets.model[1].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(targets_sh_attr[1], 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(targets_sh_attr[1])
    
    print('\tIso circle shader...', end='')
    targets.sh = sh.create('shaders/iso_circle_vert.vert',None,'shaders/iso_circle_frag.vert', targets_sh_attr, ['in_vertex', 'in_color'])
    if not targets.sh:
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
    print('\t\tOk')
    
    
    ##########################
    # eye display shader
    eye_disc.vbos     = glGenBuffers(2)
    eye_disc_sh_attr  = [8, 9]
    
    #vertices
    glBindBuffer(GL_ARRAY_BUFFER, eye_disc.vbos[0])
    glBufferData(GL_ARRAY_BUFFER, eye_disc.model[0].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(eye_disc_sh_attr[0], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(eye_disc_sh_attr[0])
    
    #colors
    glBindBuffer(GL_ARRAY_BUFFER, eye_disc.vbos[1])
    glBufferData(GL_ARRAY_BUFFER, eye_disc.model[1].astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(eye_disc_sh_attr[1], 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(eye_disc_sh_attr[1])
    
    print('\tEye disc shader...', end='')
    eye_disc.sh = sh.create('shaders/eye_disc_vert.vert',None,'shaders/eye_disc_frag.vert', eye_disc_sh_attr, ['in_vertex', 'in_color'])
    if not eye_disc.sh:
        exit(1)
    print('\t\tOk')
    
    
    ##########################
    # init projections
    cam.compute_modelview()
    cam.compute_perspective(window_w/window_h)
    
    glUseProgram(targets.sh)
    projection(targets.sh, cam.m_projection, cam.m_modelview)
    
    glUseProgram(pdp.sh)
    projection(pdp.sh, cam.m_projection, cam.m_modelview)
    
    unif_d = glGetUniformLocation(pdp.sh, "displacement")
    glUniformMatrix4fv(unif_d, 1, False, pdp.displacement)
    
    glUseProgram(object.sh)
    projection(object.sh, cam.m_projection, cam.m_modelview)
    
    unif_d = glGetUniformLocation(object.sh, "displacement")
    glUniformMatrix4fv(unif_d, 1, False, object.displacement)
    
    expe.cam    = cam


def init_eye():
    eye_disc.model = ic.circle([0,0,0], .05, 20, [1,0,0,.5])


def init():
    print("\nInit")
    init_OGL()
    init_shaders()
    init_eye()
    
    print()
    expe.print_current_conf()
    expe.save_current_conf()


################################################################################
# DISPLAY FUNCS


def display():
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    if object.display and expe.current_circle.current_target > 0:
        glUseProgram(object.sh)
        
        glBindBuffer(GL_ARRAY_BUFFER, object.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, object.model[0].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, object.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, object.model[1].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, object.vbos[2])
        glBufferData(GL_ARRAY_BUFFER, object.model[2].astype('float32'), GL_DYNAMIC_DRAW)
        
        glDrawArrays(GL_TRIANGLES, 0, len(object.model[0]))
        
    if targets.display:
        glUseProgram(targets.sh)
        
        glBindBuffer(GL_ARRAY_BUFFER, targets.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, targets.model[0].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, targets.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, targets.model[1].astype('float32'), GL_DYNAMIC_DRAW)
        
        glDrawArrays(GL_TRIANGLES, 0, len(targets.model[0]))
        
    if expe.technique == 'mouse':
        if pointer_over_window(mouse):
            cam.wiggle_pivot = mouse_intersection(mouse[0], mouse[1], cam, window_w, window_h)
    elif expe.technique == 'eye':
        if pointer_over_window(eye):
            cam.wiggle_pivot = mouse_intersection(eye[0], eye[1], cam, window_w, window_h)
            if eye_disc.display:
                eye_disc.model = ic.circle([eye[0]/window_w*2 - 1,(window_h - eye[1])/window_h*2 - 1,0], .05, 20, [1,0,0,.5])
    
    if pdp.display:
        glUseProgram(pdp.sh)
        
        glBindBuffer(GL_ARRAY_BUFFER, pdp.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, pdp.model[0].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, pdp.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, pdp.model[1].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, pdp.vbos[2])
        glBufferData(GL_ARRAY_BUFFER, pdp.model[2].astype('float32'), GL_DYNAMIC_DRAW)
        
        glDrawArrays(GL_TRIANGLES, 0, len(pdp.model[0]))
        
    if eye_disc.display:
        glUseProgram(eye_disc.sh)
        
        glBindBuffer(GL_ARRAY_BUFFER, eye_disc.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, eye_disc.model[0].astype('float32'), GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, eye_disc.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, eye_disc.model[1].astype('float32'), GL_DYNAMIC_DRAW)
        
        glDrawArrays(GL_TRIANGLES, 0, len(eye_disc.model[0]))
    
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
    elif key == b'e':
        eye_disc.display = not eye_disc.display
    #elif key == b'a':
    #    iso_circle.display_all = not iso_circle.display_all
    #    iso_circle.make_circle()
    elif key == b'o':
        object.display = not object.display
    elif key == b'p':
        pdp.display = not pdp.display
    elif key == b'c':
        print(  eye[0],eye[1],mouse[0],mouse[1]
                )
    else:
        print(key)
    
    glutPostRedisplay()


def clicks(button, state, x, y):
    
    global object
    
    mouse[0] = x
    mouse[1] = y
    
    nt = time.time()
    
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if expe.current_circle.is_current_clicked([x, window_h-y], cam.m_projection, cam.m_modelview, window_w, window_h):
                
                if expe.current_circle.current_target == 0:
                    expe.time   = nt
                    expe.mouse  = [x, y]
                else:
                    expe.new_trial(nt, [x, y])
                    expe.time   = nt
                    expe.mouse  = [x, y]
                
                if expe.current_circle.current_target >= 0:
                    p = expe.current_circle.positions[expe.current_circle.current_target]
                    object.displacement = np.identity(4)
                    object.displacement[3][0] = p[0]
                    object.displacement[3][1] = p[1]
                    glUseProgram(object.sh)
                    unif_d = glGetUniformLocation(object.sh, "displacement")
                    glUniformMatrix4fv(unif_d, 1, False, object.displacement)
                
                expe.current_circle.next()
                expe.current_circle.make_circle()
                targets.model = expe.current_circle.model
                
                if expe.current_circle.current_target == 0:
                    if not expe.next():
                        sys.exit()
                    expe.print_current_conf()
                    object.model = expe.current_model
                expe.current_circle.make_circle()
                targets.model = expe.current_circle.model
                
                
    glutPostRedisplay()


def mouse_passive(x, y):
    mouse[0] = x
    mouse[1] = y
    
    glutPostRedisplay()


def pointer_over_window(m):
    if  m[0] >= 0 and \
        m[0] <= window_w and \
        m[1] >= 0 and \
        m[1] <= window_h :
        return True
    else:
        return False


def idle():
    
    global window_w, window_h, eye
    
    window_w = glutGet(GLUT_WINDOW_WIDTH)
    window_h = glutGet(GLUT_WINDOW_HEIGHT)
    
    expe.window_w = window_w
    expe.window_h = window_h
    
    #projection update (in case the window is reshaped)
    cam.compute_perspective(window_w/window_h)
    
    #wiggling rotation
    if cam.wiggle:
        cam.wiggle_next()
    
    glUseProgram(targets.sh)
    projection(targets.sh, cam.m_projection, cam.m_modelview)
    
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
    
    #Recovering tobii events
    if expe.technique == 'eye':
        data = tob.recv_data()
        tab = np.array(data.split("_"), dtype='int')
        if tab[0] > 0 and tab[1] > 0 and tab[2] == 1:
            #eye = [tab[0]*0.66, tab[1]*.67]
            eye = [tab[0], tab[1]]
    
    glutPostRedisplay()


################################################################################
# SANDBOX


################################################################################
# MAIN

## Displaying commands
print()
print("Commands:")
print("\t'esc': exit")
print("\t'f': fullscreen")
print("\t'w': start/stop wiggle")
print("\t'p': display/hide pivot point")
print("\t'o': display/hide object")
print("\t'e': display/hide eye position")
#print("\t'a': display all/one target")


# check for command line entries
if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-u':
            expe.user_name = sys.argv[i+1]
            i += 1
        elif sys.argv[i] == '-t':
            expe.technique = sys.argv[i+1]
            if expe.technique == 'eye':
                eye_disc.display = True
            else:
                eye_disc.display = False
            i += 1
        elif sys.argv[i] == '-reload':
            expe.reload_conf()

print('Expe info')
print('\t user: ',expe.user_name)
print('\t tech: ',expe.technique)


glutInit(sys.argv)
if pl.system() == 'Linux':
    glutInitDisplayString('double rgba samples=8 depth')
else:
    glutInitDisplayString('double rgba samples=8 depth core')
glutInitWindowSize (window_w, window_h)
glutCreateWindow ('Gaze Aware Pointing')

init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(clicks)
glutPassiveMotionFunc(mouse_passive)
glutIdleFunc(idle)

glutMainLoop()
