# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 00:06:25 2019

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.colors as mcolors
import math
from math import sqrt

def createNoise(mean, variance, N,n,m):
    noiseMean=mean
    noiseVariance=variance
    noise= np.random.normal(noiseMean, noiseVariance, N)
    return noise.reshape(n,m)

"""
--------------------------------------------------------------------------------------
Parameters:	mode : String.
                    Value to choose mode of perception between "Normal", "Noise", "No"
--------------------------------------------------------------------------------------
"""

class sound_perception():
     def  __init__(self,  mode):
        sound_perc=[[0.4 , 0.4 , 0.4 , 0.4 , 0.4 , 0.4 , 0.4],
                         [0.4 , 0.4 , 0.4 , 0.4 , 0.4 , 0.4 , 0.4],
                         [0.4 , 0.5 , 0.5 , 0.5 , 0.5 , 0.4 , 0.4],
                         [0.5 , 0.6 , 0.6 , 0.6 , 0.6 , 0.5 , 0.5],
                         [0.6 , 0.7 , 0.7 , 0.7 , 0.7 , 0.6 , 0.5],
                         [0.6 , 0.7 , 0.9 , 1. , 0.8 , 0.7 , 0.5],
                         [0.7 , 0.8 , 0.9 , 1. , 1. , 0.8 , 0.6]]
        if(mode == "Normal"):
            self.perception=sound_perc
            #self.color_map()
        elif(mode == "Noise"):
            noise=createNoise(0, 0.2, 49, 7, 7)
            self.perception=sound_perc+noise
            #self.color_map()
        elif(mode == "NO"):
            self.perception= np.zeros((7, 7), int)
        #print(self.perception)
			
     def reading_sound(self,x0,y0):
        return self.perception[y0][x0] 
        #return self.perception[len(self.perception[0])-1-x0][len(self.perception)-1-y0]
    
     def color_map(self): 
       figure=plt.figure(1)
       plt.imshow(self.perception, interpolation='nearest', origin='lower')
       plt.title("Robot's perception of the Sound")
       plt.colorbar()
	   

