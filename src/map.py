# map.py
#
# Omkar H. Ramachandran
# omkar.ramachandran@colorado.edu
#
# Map building function
#

import numpy as np


class Map:
    def __init__(self,Nareas,NTILES):
        self.Area = np.ones([NTILES,NTILES]) 
        self.Ntiles = NTILES
        self.Nareas = Nareas
    def gen_area(self,centerx,centery,R):
        x = np.linspace(1,self.Ntiles,self.Ntiles)
        y = np.linspace(1,self.Ntiles,self.Ntiles)

        # Create central room
        th = np.linspace(0,2*np.pi,75)
        ii = np.where(abs(x-centerx) <= R[0])
        jj = np.where(abs(y-centery) <= R[1])
        
        x = x.astype(int)
        y = y.astype(int)
        kk = np.where(x[ii] >= self.Ntiles) 
        x[kk] = self.Ntiles -1
        kk = np.where(x[ii] < 0) 
        x[kk] = 0
        kk = np.where(y[ii] >= self.Ntiles) 
        y[kk] = self.Ntiles -1
        kk = np.where(y[ii] < 0) 
        y[kk] = 0

        X,Y = np.meshgrid(x[ii],y[jj])
        
        
        self.Area[X,Y] = 0
    def gen_map(self):
        for i in range(self.Nareas):
            centerx = np.random.uniform(low=0.2,high=0.8)*self.Ntiles
            centery = np.random.uniform(low=0.2,high=0.8)*self.Ntiles
            Rx = 0.2*self.Ntiles/6.+0.2*np.random.uniform()*self.Ntiles/10.
            Ry = 0.2*self.Ntiles/6.+0.2*np.random.uniform()*self.Ntiles/10.
            print(centerx,centery,[Rx,Ry])
            self.gen_area(centerx,centery,[Rx,Ry])
