import Inputs_function as IF
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np
import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner
import Robot_Perception_Light as RPL
import Robot_Perception_Sound as RPS
import time
import threading
import random
import neural
import Model as m

"""
Transpose a matrix because its position [x][y] is different from (x,y) position in grid
Plots the colormap
"""
def color_map(matrix,noOfExp,mode):
    x = [0, 1 , 2 , 3 , 4 , 5 , 6 ]
    cmap=np.transpose(matrix)
    plt.imshow(cmap, interpolation='nearest', origin='lower')
    plt.title("Results" + "\n"+str(noOfExp) + " Experiments per cell.  Mode : " + mode)
    plt.colorbar()
    plt.show()

noOfExperiments=100
max_time= 10#sec
N=1
accuracy=np.zeros((7, 7), int)

"""
This variable changes the mode of the Robot's perception.
Please choose between :  "No Vision", "No Sound", "Noise - Vision", "Noise - Sound"
"""
mode="Noise - Sound"

for x in range (0,7):
	for y in range(0,7):
		for experiments in range(0,noOfExperiments):
			start_time=time.time()
			model = m.Model(N,7,7,x,y,mode)
			print("Starting Position : "+ str([x,y]))
			print("experiment : "+ str(experiments))
			# Run the model
			while True:
				#show_grid(model)
				running_time=time.time()-start_time
				model.step()
				#steps.append(j)
				
				agent_perc = model.datacollector.get_agent_vars_dataframe()
				#print(agent_perc)			
				#print("agent perc : "+ str(agent_perc['Position'][-1]))
		
				if(running_time>=max_time or agent_perc['Position'][-1]==(3,6)):
					#print(running_time)
					if agent_perc['Position'][-1]==(3,6):
						accuracy[x][y]+=1
					print("Result of trial : "+ str(accuracy[x][y]))
					print("Time of current trial: " + str(running_time))
					break
	
print(accuracy)
color_map((accuracy/noOfExperiments).tolist(),noOfExperiments, mode)



