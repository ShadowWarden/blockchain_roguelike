# item.py
# Omkar H. Ramachandran
# omkar.ramachandran@colorado.edu
#
# Items!
#

import pygame
import numpy as np
from pygame.locals import *
import text
import os

class Item:
    """ Items have the following stats:
        weight
        damage
        cost
        base AC
    """
    def define(self,itemid,name,flavor,weight,damage,cost,ac):
        self.id = itemid
        self.name = name
        self.flavor = flavor
        self.weight = weight
        self.damage = damage
        self.cost = cost
        self.ac = ac

I = [Item() for i in range(1)]
I[0].define(0,"Longsword","A five foot long hunk of steel. The staple of adventurers across the land",4,8,15,0)
