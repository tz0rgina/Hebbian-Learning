
import numpy as np

def Inputs_Function(agent_perc,light_readings):
    inputs=[0,0,0,0,0,0,0]	
    s_list=agent_perc['Sound Perception'].tolist()
    direction=agent_perc['Behaviour'].tolist()
    if len(s_list)>=31:
        if s_list[-1]>s_list[-1-30]-0.03:
            inputs[0]=1
        elif s_list[-1]<s_list[-1-30]-0.03:
            inputs[1]=1
        elif s_list[-1]>=s_list[-1-30]:
            inputs[2]=1
        elif s_list[-1]<=s_list[-1-30]:
            inputs[3]=1
    if len(light_readings)>=11 :
        if light_readings[-1]<0.01:
            #print('----------------------------------------')
            inputs[6]=1
        elif light_readings[-1]<light_readings[-1-10]-0.01 and direction[-1]=='backward':
            inputs[5]=1
        elif light_readings[-1]<light_readings[-1-10]-0.01 and direction[-1]=='forward':
            inputs[6]=1
        elif  direction[-1]=='backward':
            inputs[5]=1
        elif direction[-1]=='forward':
            inputs[4]=1
    return inputs
        
        