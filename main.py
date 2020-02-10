import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from math import atan2

from camera import *
from world import *


def main():
    pygame.init()
    height = 700
    width = 1000
    display = (width, height)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.set_pos(width / 2, height / 2)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    
    camera = Camera(prop=(width, height))
    world = World()

    
    clock = pygame.time.Clock()
    exit = True
    wall = True

    while exit:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        mousepos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        #EXIT GAME
        if keys[pygame.K_ESCAPE]:
            exit = False

        
        #ROTATE CAMERA AND RESET MOUSE POSITION
        if wall:
            camera.rotate(mouse_dx, mouse_dy)

        wall = True
        if mousepos[0] <= 1:
            pygame.mouse.set_pos(width, mousepos[1])
            wall = False
        if mousepos[0] >= width-1:
            pygame.mouse.set_pos(0, mousepos[1])
            wall = False
        if mousepos[1] <= 1:
            pygame.mouse.set_pos(mousepos[0], height)
            wall = False
        if mousepos[1] >= height-1:
            pygame.mouse.set_pos(mousepos[0], 0)
            wall = False

        #move up/down
        fwd = -1 * (keys[K_w]-keys[K_s])
        strafe = 1 * (keys[K_a]-keys[K_d])
        if abs(fwd) or abs(strafe):
            m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
            camera.move(fwd, strafe)

        
        if event.type == pygame.MOUSEBUTTONUP:
            bm4, bm5 = 0, 0
            if event.button == 5:
                bm5 = 1
            if event.button == 4:
                bm4 = 1

            mup = -2 * (bm5-bm4)
            if abs(mup):
                mup = mup * 4
                glTranslatef(0, mup, 0)
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        world.draw_objects()
        pygame.display.flip()
        

if __name__ == '__main__':
    main()


