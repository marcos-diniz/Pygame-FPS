from math import sqrt, atan2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

__all__ = ["Camera"]


class Camera:
    def __init__(self, prop=(1,1)):
        self.speed_move = 6
        self.sensibility = 0.25
        self.prop = prop
        self.buffer = 2
        self.starty = 30
        self.startx = 0
        self.pos = [0, self.starty, 0]
        
        gluPerspective(90, (self.prop[0] // self.prop[1]), 0.1, 10000)
        glTranslatef(0, -self.starty, 0)
    
    def move(self, fwd, strafe):
        fwd *= self.speed_move
        strafe *= self.speed_move
        m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
        glTranslatef(fwd*m[2], 0, fwd*m[10])#FRONT/BACK-MOVE
        glTranslatef(strafe*m[0], 0, strafe*m[8])#LEFT/RIGHT-MOVE
        #Save New Position
        self.pos[0] += fwd*m[2] + strafe*m[0]
        self.pos[2] += fwd*m[10] + strafe*m[8]
    
    def rotate(self, mouse_dx, mouse_dy):
        _buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = (-1 * np.mat(_buffer[:3, :3]) * np.mat(_buffer[3, :3]).T).reshape(3, 1)
        #-camera_center_in_3d
        glTranslate(c[0], c[1], c[2])
        
        m = _buffer.flatten()
        angle_x = mouse_dx * self.sensibility
        angle_y = mouse_dy * self.sensibility
        
        glRotate(angle_x, m[1], m[5], m[9])  # [1]
        glRotate(angle_y, m[0], m[4], m[8])  # [1]
        # compensate roll - make sure camera's "up" is actually upwards
        glRotate(atan2(-m[4], m[5]) * 57.29577, m[2], m[6], m[10])
        #camera_center_in_3d
        glTranslate(-c[0], -c[1], -c[2])
    