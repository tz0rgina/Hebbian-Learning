import numpy as np
import random

"""
def diff(list1, list2):
    return [x1 - x2 for (x1, x2) in zip(list1, list2)]

def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())
"""

def activation_function(weights, inputs):
    activations=[]
    #print(weights)
    for weight in weights :
        #print(weight)
        #print(inputs)
        #print(np.inner(weight, inputs))
        activations.append(1/(1+np.exp(-np.inner(weight, inputs))))
    #print("activations = " + str(activations))
    out=activations.index(max(activations))
    #print(out)
    ties=[i for i, x in enumerate(activations) if x==activations[out]]
    #print(ties)
    return random.choice(ties)
        
def right_activations(inputs):
    output_s=-2
    output_l=-1
    right_output=[0 , 0 , 0 , 0]
    for i in range(0,len(inputs)):
        if(inputs[i]==1):
            if (i<=3):
                output_s=i
            else:
                output_l=i-4
    #print([output_s , output_l])
    if (output_s == output_l):
        right_output[output_s]=1
    elif (output_s == -2 and output_l>=0):
        right_output[output_l]=1
    elif (output_l == -1 and output_s>=0):
        right_output[output_s]=1
    else:
        if (output_l>=0 and output_s>=0):
            prob=np.random.random_sample()
            #print(prob)
            if prob<=0.5:
                right_output[output_s]=1
            else:
                right_output[output_l]=1
    return right_output
            
     
def oja_rule(weights, inputs, outputs, hta):
    w=np.matrix.copy(weights)
    for i in range(0,len(weights)):
        for j in range(0,len(weights[0])):
            s=0
            for k in range (0, i):
                s=s+weights[k][j]*outputs[k]
                #print([i,j,k,s])
            w[i][j]+= hta*outputs[i]*(inputs[j]-s)
    return w

#test right activations
possible=[[0,0,0,0,0,0,0],
          [1,0,0,0,1,0,0],
          [1,0,0,0,0,1,0],
          [1,0,0,0,0,0,1],
          [0,1,0,0,1,0,0],
          [0,1,0,0,0,1,0],
          [0,1,0,0,0,0,1],
          [0,0,1,0,1,0,0],
          [0,0,1,0,0,1,0],
          [0,0,1,0,0,0,1],
          [0,0,0,1,1,0,0],
          [0,0,0,1,0,1,0],
          [0,0,0,1,0,0,1],
          [1,0,0,0,0,0,0],
          [0,1,0,0,0,0,0],
          [0,0,1,0,0,0,0],
          [0,0,0,1,0,0,0],
          [0,0,0,0,1,0,0],
          [0,0,0,0,0,1,0],
          [0,0,0,0,0,0,1]]
"""
for p in possible:
    print(p)
    print(right_activations(p))
    print("")

#test weights
weights = np.array([[0.01, 0.77, 0.01, 0.01, 0.85, 0.01, 0.01],
 [0.01, 2.14 ,0.01, 0.01, 0.77, 1.41, 0.01],
 [0.01 ,0.01 ,0.01, 0.01, 0.01, 0.01, 0.1 ],
 [0.01 ,0.01, 0.01, 0.01, 0.01, 0.01, 0.01]])
inputs = [0, 1, 0, 0, 1, 0, 0]
outputs=right_activations(inputs)
print(outputs)
print(oja_rule(weights, inputs, outputs, 0.01))
"""