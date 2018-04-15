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
       
        x[ii[0][int(len(ii[0])/2)]] = 3
        y[ii[0][int(len(ii[0])/2)]] = 3

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
        coords = np.array([-1,-1])
        PlayerStart = np.zeros([2])
        for i in range(self.Nareas):
            centerx = np.random.uniform(low = 0.2, high=0.8)*self.Ntiles
            centery = np.random.uniform(low = 0.2, high=0.8)*self.Ntiles
            if(coords[0] > 0):
                PlayerStart = np.array([centerx,centery])
                x = np.linspace(coords[0],centerx,101)
                y = coords[1] + (centery-coords[1])/(centerx-coords[0])*(x-coords[0])
                x = x.astype(int)
                y = y.astype(int)
                self.Area[x,y] = 0
                flag = 0
                for i in range(len(x)):
                    if(self.Area[x[i],y[i]+1] == 1):
                        flag += 1
                    if(self.Area[x[i],y[i]-1] == 1):
                        flag += 1
                    if(self.Area[x[i]+1,y[i]] == 1):
                        flag += 1
                    if(self.Area[x[i]-1,y[i]] == 1):
                        flag += 1 
                    if(flag == 3):
                        self.Area[x[i],y[i]+1] = 0
                        self.Area[x[i],y[i]-1] = 0
                        self.Area[x[i]+1,y[i]] = 0
                        self.Area[x[i]-1,y[i]] = 0
 
            Rx = np.random.uniform(low = 0.4,high = 1.)*self.Ntiles*0.15
            Ry = np.random.uniform(low = 0.4,high = 1.)*self.Ntiles*0.15
            self.gen_area(centerx,centery,[Rx,Ry])
            coords[0] = centerx
            coords[1] = centery
        return PlayerStart
