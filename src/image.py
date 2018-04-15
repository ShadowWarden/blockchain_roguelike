# image.py
#
# Omkar H. Ramachandran
# omkar.ramachandran@colorado.edu
#
# Images!
#

import pygame
from pygame.locals import *
import os
import numpy as np

def load_png(name):
    """ Load image """
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image, image.get_rect()
