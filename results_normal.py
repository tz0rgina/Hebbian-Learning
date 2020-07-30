import numpy as np
import matplotlib.pyplot as plt

results=[]
#1 experiments
noOfExp=1
results.append([[0,0,1,0,0,0,1],
         [0,0,1,1,0,1,1],
         [0,0,0,0,1,1,1],
         [0,1,1,0,1,1,1],
         [0,1,0,1,1,1,1],
         [0,0,0,0,1,0,0],
         [0,0,0,1,0,1,0]])
#print(results)

#21 experiments
noOfExp+=1
results.append([[0,0,0,0,0,1,0],
         [0,0,0,0,0,1,1],
         [0,0,0,0,1,0,1],
         [0,0,0,0,1,1,1],
         [0,0,0,1,0,1,1],
         [0,0,0,0,0,1,1],
         [0,1,0,1,0,0,0]])
#print(results)

#1 experiments
noOfExp+=1
results.append([[0, 0, 0, 0, 1, 1, 0],
                [1, 1, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 0, 1, 1],
                [0, 0, 0, 0, 1, 1, 1],
                [1, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 1, 0, 1],
                [0, 0, 0, 0, 0, 1, 0]])
#print(results)				

noOfExp+=6
results.append([[0, 0, 0, 2, 0, 2, 2],
                [0, 0, 1, 1, 2, 1, 2],
                [0, 2, 0, 2, 3, 3, 4],
                [1, 0, 1, 1, 5, 4, 6],
                [0, 0, 0, 3, 1, 3, 4],
                [1, 1, 1, 2, 1, 3, 0],
                [0, 1, 1, 1, 2, 5, 4]])
				
noOfExp+=6
results.append([[0, 1, 0, 1, 2, 1, 3],
                [0, 1, 1, 2, 2, 2, 2],
                [1, 0, 1, 1, 2, 3, 4],
                [0, 1, 1, 3, 5, 3, 6],
                [1, 2, 1, 2, 0, 2, 4],
                [0, 1, 1, 0, 1, 3, 2],
                [0, 1, 1, 0, 2, 1, 3]])

def final_results(results , noOfExp):
    final= np.zeros((7, 7), int)
    print(results)
    for result in results:
        print(result)
        #final=final+result
        # iterate through rows 
        for i in range(len(result)):    
        # iterate through columns 
            for j in range(len(result[0])): 
                final[i][j] = result[i][j] + final[i][j] 
    print(final)
    final=final/noOfExp 
    return(final)
	
def color_map(matrix):
    x = [0, 1 , 2 , 3 , 4 , 5 , 6 ]
    cmap=np.transpose(matrix)
    plt.imshow(cmap, interpolation='nearest', origin='lower')
    plt.title("Results." + str(noOfExp) + " Experiments per cell.  Mode : No Sound")
    plt.colorbar()
    plt.show()

color_map(final_results(results , noOfExp).tolist())
    
		 
