# init.py
# 
# Omkar H. Ramachandran
# omkar.ramachandran@colorado.edu
#
# Pygame init
#

import pygame
from pygame.locals import *
import os
import numpy as np
import json
import image
import text
import move
import itertools

import client
import state as S

XLIM = 600
YLIM = 600
NTILES = 10
dTILE = 60

Map = np.zeros([NTILES,NTILES])


Map[0,:] += 1
Map[-1,:] += 1
Map[1:-1,0] += 1
Map[1:-1,-1] += 1
Map[5,5] += 2
Map[8,8] += 3

print(Map)

def main():
    """ Main program """
    # Base inits. Safe to do multiple times. If fail, fails quietly
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((XLIM,YLIM))
    pygame.display.set_caption("Basic Pygame game")
    myfont = pygame.font.SysFont('Comic Sans MS', 40)

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    # Colour's in RGB
    background.fill((250,250,250))
    #background = pygame.image.load("./artlib/bg.jpg")
    

    # Display text
    text.showtext(background,"Hello World!",XLIM/2,YLIM/2,50,[10,0,0])  
    brick_tile = pygame.image.load("../artlib/wall.png")
    brick_tile = pygame.transform.scale(brick_tile,(dTILE,dTILE))
    floor_tile = pygame.image.load("../artlib/floor.png")
    floor_tile = pygame.transform.scale(floor_tile,(dTILE,dTILE))
    charac_tile = pygame.image.load("../artlib/charac.png")
    charac_tile = pygame.transform.scale(charac_tile,(dTILE,dTILE))
    orc_tile = pygame.image.load("../artlib/orc.png")
    orc_tile = pygame.transform.scale(orc_tile,(dTILE,dTILE))


    def tile_background():
        for x,y in itertools.product(range(0,XLIM,dTILE),range(0,YLIM,dTILE)):
            if(Map[int(x/dTILE),int(y/dTILE)] == 1):
                screen.blit(brick_tile,(x,y))
            else:
                screen.blit(floor_tile,(x,y))
    # Blit everything to screen
    
    def place_char():
        ii = np.where(Map == 2)
        screen.blit(charac_tile,(dTILE*ii[0],dTILE*ii[1]))
    
    def place_npc():
        ii = np.where(Map == 3)
        screen.blit(orc_tile,(dTILE*ii[0],dTILE*ii[1]))

    screen.blit(background,(0,0))

    res1 = client.create_state(0)

    moveres = 1
    moved = 1
    angle = 90
    Res = client.check(res1)
    print(Res)
    offset = 0
    while 1:
        time = pygame.time.get_ticks()
        if(time +offset*1000> 5000):
            Res = client.check(res1)
            offset -= 5
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move.Move(Map,2)
                    dtheta = 0-angle
                    charac_tile = pygame.transform.rotate(charac_tile,dtheta)
                    angle = 0
                    moved = 1
                elif event.key == pygame.K_RIGHT:
                    move.Move(Map,3) 
                    dtheta = 180-angle
                    charac_tile = pygame.transform.rotate(charac_tile,dtheta)
                    angle = 180
                    moved = 1
                elif event.key == pygame.K_UP:
                    moveres = move.Move(Map,0) 
                    dtheta = 270-angle
                    charac_tile = pygame.transform.rotate(charac_tile,dtheta)
                    angle = 270
                    moved = 1
                elif event.key == pygame.K_DOWN:
                    move.Move(Map,1) 
                    dtheta = 90-angle
                    charac_tile = pygame.transform.rotate(charac_tile,dtheta)
                    angle = 90
                    moved = 1 
                elif event.key == pygame.K_k:
                    res1 = client.create_fake_state(0)
            if event.type == QUIT:
                return
        if(moved == 1):
            tile_background()
            place_char()
            place_npc()
            if(moveres == 0): 
                text.showtext(background,"There's a wall there!",XLIM/2,YLIM/2,50,[10,0,0])  
            if(Res['index'] == -2):
                label = myfont.render("You cheat... -_-",1,(255,255,0))
                screen.blit(label,((XLIM-30)/2,YLIM/2))
            pygame.display.flip()
            moved = 0
 

if __name__ == '__main__': main()
