import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from math import atan2
from camera import *
from wavefrontloader import *

def main():
    pygame.init()
    width, height = 1000, 700 
    display = (width, height)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.set_pos(width // 2, height // 2)
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    
    camera = Camera(fov=60, sensibility=0.35, speed=6, screen_size=display,
     nearclip=0.1, farclip=10000)
    wavefront_obj = WavefrontObject('wavefronts/map.obj')

    clock = pygame.time.Clock()
    exit = True
    paused = True

    while exit:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    paused = not paused

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        mousepos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        #stop the while loop
        if keys[pygame.K_ESCAPE]:
            exit = False

        if not paused:
            camera.move(keys[K_w], keys[K_s], keys[K_a], keys[K_d], keys[K_DOWN], keys[K_UP])

            camera.rotate(mouse_dx, mouse_dy)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        #DRAWOBJECTS
        wavefront_obj.draw()
        pygame.display.flip()
        
if __name__ == '__main__':
    main()


