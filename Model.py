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

class Robot(Agent):
    def  __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.views=['north','south','west','east']
        self.view=random.choice(self.views)
        self.behaviours=['forward','backward']
        self.behaviour=random.choice(self.behaviours)
        #self.weights=np.random.rand(4,7)
        
        self.weights=np.array([[0.01,0.01,0.01,0.01,0.01,0.01,0.01],
                      [0.01,0.01,0.01,0.01,0.01,0.01,0.01],
                      [0.01,0.01,0.01,0.01,0.01,0.01,0.01],
                      [0.01,0.01,0.01,0.01,0.01,0.01,0.01]])
        self.input=[]
        self.output=[]
        self.iteration=0
        self.light_readings=[]
        #print([self.view, self.behaviour])        

    def findNextPosition(self):
        if self.behaviour=='forward':
            if self.view=='north':
                new_position=(self.pos[0],self.pos[1]+1)
            elif self.view=='south':
                new_position=(self.pos[0],self.pos[1]-1)
            elif self.view=='west':
                new_position=(self.pos[0]-1,self.pos[1])
            elif self.view=='east':
                new_position=(self.pos[0]+1,self.pos[1])
        else:
            if self.view=='north':
                new_position=(self.pos[0],self.pos[1]-1)
            elif self.view=='south':
                new_position=(self.pos[0],self.pos[1]+1)
            elif self.view=='west':
                new_position=(self.pos[0]+1,self.pos[1])
            elif self.view=='east':
                new_position=(self.pos[0]-1,self.pos[1])
        return new_position
    
    def turn_right(self):
        if self.view=='north':
            self.view='east'
        elif self.view=='south':
            self.view='west'
        elif self.view=='west':
            self.view='north'
        elif self.view=='east':
            self.view='south'
            
    def turn_left(self):
        if self.view=='north':
            self.view='west'
        elif self.view=='south':
            self.view='east'
        elif self.view=='west':
            self.view='south'
        elif self.view=='east':
            self.view='north'
            
    def invert_behaviour(self):
        if self.behaviour=='forward':
            self.behaviour='backward' 
        else: 
            self.behaviour='forward'
        
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=True)
        #print(possible_steps)
        new_position=self.pos
        if self.output[0] == 1:
            new_position = self.findNextPosition()
        if self.output[1] == 1:
            self.invert_behaviour()
            new_position = self.findNextPosition() 
        elif self.output[2] == 1:
            self.turn_left()
            new_position = self.findNextPosition()
        elif self.output[3] == 1:
            self.turn_right()
            self.invert_behaviour()
            #new_position=self.findNextPosition()   
        #print(new_position)
        if new_position in possible_steps:
            self.model.grid.move_agent(self, new_position)
        
    def step(self):# the agent function when it is activated
        #print(self.sound_perc)
        #print(self.light_perc)
        position=self.pos
        memory=self.model.datacollector.get_agent_vars_dataframe()
        #print("self.pos : "+str(self.pos))
		
		#code for imprint
        if (self.iteration>=120 and self.iteration%120 == 0):
            self.light_perc = self.model.robot_light.reading_light(position[0],position[1])
            self.light_readings.append(self.model.robot_light.reading_light(position[0],position[1]))
        else:
            self.light_perc=memory['Light Perception'].tolist()[-1]
			
        self.sound_perc = self.model.robot_sound.reading_sound(position[0],position[1])
        self.input=IF.Inputs_Function(memory,self.light_readings)
        #print("input = "+ str(self.input))
		
        activation=neural.activation_function(self.weights,self.input)
        #print("right_activations = " + str((neural.right_activations(self.input))))
        self.output=[0,0,0,0]
        self.output[activation]=1
        #print("output = "+str(self.output))
        new_weights=neural.oja_rule(self.weights, self.input, neural.right_activations(self.input), 0.01)
        self.weights=[]
        self.weights=new_weights
        #print("weights = " + str(self.weights))
        # The agent's step will go here.
        self.move()
        self.iteration+=1
        time.sleep(0.05)
        #print("")

"""
Τhis model is made for more than one agents, but it is tested with unique robot agent.  
"""
       
class Model(Model):
    def __init__(self, N, width, height , x , y, mode):
        sound_mode, light_mode=self.choose_mode(mode)
        self.robot_sound=RPS.sound_perception(sound_mode)
        #self.robot_sound.plot_sound_perception()
        self.robot_light=RPL.light_perception(light_mode)
        #self.robot_light.plot_light_perception()
        self.num_agents = N
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
		
        # Create agents
        for i in range(self.num_agents):
            a = Robot(i, self)
            self.schedule.add(a)
                
            # Add the agent to a random grid cell
            #x = self.random.randrange(self.grid.width)
            #y = self.random.randrange(self.grid.height)
            #print(x,y)
            self.grid.place_agent(a, (x, y))
            a.sound_perc = self.robot_sound.reading_sound(x,y)
            a.light_perc = self.robot_light.reading_light(x,y)
            a.light_readings.append(a.light_perc)
            self.running = True    
           
        self.datacollector = DataCollector(
            agent_reporters={"Sound Perception": "sound_perc","Light Perception": "light_perc",
                             "View":"view", "Behaviour":"behaviour","Position":"pos", 
                             "Inputs":"input","Outputs":"output", "Weights":"weights",
                             "Iterations":"iteration"})
     

    def step(self):
       self.datacollector.collect(self)
       self.schedule.step()
	   
    def choose_mode(self,mode):
        if (mode=="Normal"):
            return "Normal","Normal"
        elif (mode=="No Vision"):
            return "Normal","NO"
        elif (mode=="No Sound"):
            return "NO","Normal"
        elif (mode=="Noise - Vision"):
            return "Normal","Noise"
        elif (mode=="Noise - Sound"):
            return "Noise","Normal"         
     
def show_grid(model,j):
   figure=plt.figure(j)
   agent_counts = np.zeros((model.grid.width, model.grid.height))
   for cell in model.grid.coord_iter():
       cell_content, x, y = cell
       # print(cell_content)
       agent_count = len(cell_content)
       agent_counts[y][x] = agent_count
   _=plt.imshow(agent_counts, interpolation='nearest', origin='lower')
  
  
  
"""
-----------------------
Runs single experiment.
----------------------
""Could plot perception for every position of grid (Need of uncomment #self.color_map() in Robot_Perception_Light
and Robot_Perception_Sound)
""Plots perception during steps
""Able to print the data frame with all experiment's information 
"""
def single_experiment(x ,y, mode):

    N=1
    inputs=[]
    start_time=time.time()
    model = Model(N , 7 ,7 , x , y, mode) 
    i=0
    while True:
        print("step : " + str(i))
        show_grid(model,2)
        model.step() 
        running_time=time.time()-start_time
        i+=1
        agent_perc = model.datacollector.get_agent_vars_dataframe()
        if(running_time>=20 or agent_perc['Position'][-1]==(3,6)):             
            break
    running_time=time.time()-start_time
    print("runningtime : " + str(running_time))
    #inputs.append(IF.Inputs_Function(agent_perc))  
    #print(agent_perc[['View','Position', 'Behaviour', 'Light Perception','Sound Perception']][0:100])
    figure=plt.figure(3)
    _=plt.title('Sound Perception during steps')
    steps=agent_perc['Iterations'].tolist()
    _=plt.axis([steps[0], steps[-1], 0.4,1.])
    _=plt.plot(steps,agent_perc['Sound Perception'].tolist())
    figure=plt.figure(4)
    _=plt.title('Light Perception during steps')   
    _=plt.axis([steps[0], steps[-1], 0.,60.])
    _=plt.plot(steps,agent_perc['Light Perception'].tolist())
    agent_perc.head()
    plt.show()
       
"""
------------------------------------------------------------------------------------
Uncomment the above for single experiment for a certain initial position and mode
------------------------------------------------------------------------------------ 
Variable mode changes the mode of the Robot's perception.
Please choose between :  "No Vision", "No Sound", "Noise - Vision", "Noise - Sound"
"""
#mode="Normal"
#single_experiment(3 ,5, mode)


