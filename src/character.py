# character.py
#
# Omkar H. Ramachandran
# omkar.ramachandran@colorado.edu
#
# Character class definitions
#

import item
import numpy as np

class character:
    def __init__(self,st,iq,dex,wiz,co,ch,hitdice,attack):
        self.st = st
        self.iq = iq
        self.dex = dex
        self.wiz = wiz
        self.co = co
        self.ch = ch
        self.attack = 1.
        self.encumb = 0.
        self.compute_mod()
        # Compute starting health
        self.hpts = hitdice+self.comod
        self.curhpts = self.hpts
        self.ac = 10+self.dexmod
        self.exp = 0
        self.item = []
        self.wpndamage = 0.0
        self.equipped = []
    def compute_mod(self):
        self.stmod = int((self.st-10)/2.)
        self.dexmod = int((self.dex-10)/2.)
        self.iqmod = int((self.iq-10)/2.)
        self.wizmod = int((self.wiz-10)/2.)
        self.comod = int((self.co-10)/2.)
        self.chmod = int((self.ch-10)/2.)
    def additem(self,itemid):
        (self.item).append(itemid)
        self.encumb += item.I[itemid].weight
    def equipitem(self,itemid):
        (self.equipped).append(itemid)
        self.wpndamage += item.I[itemid].damage
        self.ac += item.I[itemid].ac
    def unequipitem(self,itemid):
        ii = np.where(np.array(self.item) == itemid)
        del self.item[ii[0][0]]
        self.wpndamage -= item.I[itemid].damage
        self.ac -= item.I[itemid].ac
    def dropitem(self,itemid):
        ii = np.where(np.array(self.item) == itemid)
        self.encumb -= item.I[itemid].weight
        del self.item[ii[0][0]]
    def attack(self):
        return int(np.random.uniform()*19+1)+self.attack+self.st
    def damage(self):
        dam = int(np.random.uniform()*(self.wpndamage-1)+1)+self.stmod
        if(dam >= 0):
            return dam
        else:
            return 0
