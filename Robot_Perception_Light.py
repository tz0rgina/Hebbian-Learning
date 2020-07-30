
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.colors as mcolors

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

class light_perception():
    def  __init__(self, mode):
        light_perc=[[20. , 25. , 25. , 25. , 25. , 25. , 20.],
                    [20. , 25. , 25. , 25. , 25. , 25. , 20.],
                    [25. , 25. , 25. , 25. , 25. , 25. , 20.],
                    [20. , 25. , 25. , 25. , 25. , 25. , 20.],
                    [20. , 25. , 40. , 40. , 40. , 25. , 10.],
                    [10. , 25. , 50. , 50. , 50. , 25. , 10.],
                    [0. , 10. , 50. , 60. , 50. , 10. , 0.]]
        if(mode == "Normal"):
            self.perception=light_perc
            #self.color_map()
        elif(mode == "Noise"):
            noise=createNoise(0,20, 49, 7, 7)
            self.perception=light_perc+noise
            #self.color_map()
        elif(mode == "NO"):
            self.perception= np.zeros((7, 7), int)
			
        
    def reading_light(self,x0,y0):
        return self.perception[y0][x0]
    
    def color_map(self):  
        figure=plt.figure(0)
        plt.imshow(self.perception, interpolation='nearest', origin='lower')
        plt.title("Robot's perception of the Light")
        plt.colorbar()
        
		

