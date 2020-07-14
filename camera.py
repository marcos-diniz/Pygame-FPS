from math import sqrt, atan2
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

__all__ = ["Camera"]

class Camera:
    def __init__(self, fov, sensibility, speed, screen_size, nearclip, farclip):
        self._speed_move = speed
        self._sensibility = sensibility
        self._aspect = (screen_size[0]/screen_size[1])
        self._screen_size = screen_size
        self._fov = fov
        self._location = [-839.2773821545411,
                          -116.64508592611948,
                          479.71180621362146]

        self._center = None
        self._rotation = [0,0,0]
        self._start = 0
        self._nearclip = nearclip
        self._farclip = farclip

        glMatrixMode(GL_PROJECTION)
        gluPerspective(self._fov, self._aspect, self._nearclip, self._farclip)
        glMatrixMode(GL_MODELVIEW)
        
        glTranslatef(self._location[0], self._location[1], self._location[2])
        self.rotate(-350.02116749999999, 0.4055126249999996)

    def rotate(self, mouse_dx, mouse_dy):
        _buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        self._center = (-1 * np.mat(_buffer[:3,:3]) * \
            np.mat(_buffer[3,:3]).T).reshape(3,1)

        glTranslate(self._center[0],self._center[1],self._center[2])
        
        m = _buffer.flatten()
        
        anglex = mouse_dx * self._sensibility
        angley = mouse_dy * self._sensibility

        glRotatef(anglex, m[1],m[5],m[9])
        glRotatef(angley, m[0],m[4],m[8])

        self._rotation[0] += anglex
        self._rotation[1] += angley
        
        glRotated(-math.atan2(-m[4],m[5]) * \
            57.295779513082320876798154814105 ,m[2],m[6],m[10])
        glTranslate(-self._center[0],-self._center[1],-self._center[2])

    def move(self, front=False, back=False, left=False, right=False,
     down=False, up=False):
        #Move fron, back, left, right, down,up
        fwd = self._speed_move * (front-back) 
        strafe = self._speed_move * (left-right)
        mup = self._speed_move * (down-up)
        
        if abs(fwd) or abs(strafe) or abs(mup):
            m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
            glTranslate(fwd*m[2],fwd*m[6],fwd*m[10])
            glTranslate(strafe*m[0],strafe*m[4],strafe*m[8])
            glTranslate(0, mup, 0)
            #save new position
            self._location[0] += fwd*m[2] + strafe*m[0]
            self._location[1] += fwd*m[6] + strafe*m[4] + mup
            self._location[2] += fwd*m[10] + strafe*m[8]
