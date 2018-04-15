# text.py
# 
# Omkar H. Ramachandran
# omkar.ramachandran@colorado.edu
#
# All text rendering commands
#

import pygame
from pygame.locals import *
import os
import numpy as np

def showtext(background,string,pos_x,pos_y,size,color):
    font = pygame.font.Font(None,size)
    text = font.render(string,1,(color[0],color[1],color[2]))
    textpos = text.get_rect()
    textpos.centerx = pos_x
    textpos.centery = pos_y
    background.blit(text,textpos)
