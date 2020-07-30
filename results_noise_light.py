import numpy as np
import matplotlib.pyplot as plt

results=[]
#4 experiments
noOfExp=4
results.append([[0, 1, 0, 1, 3, 3, 2],
                [1, 0, 0, 0, 0, 1, 1],
                [1, 1, 1, 1, 0, 2, 2],
                [1, 0, 1, 2, 2, 1, 4],
                [1, 0, 0, 2, 2, 1, 4],
                [1, 0, 0, 1, 0, 3, 2],
                [1, 0, 1, 0, 0, 1, 2]])
			
 
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
    plt.title("Results" + "\n"+str(noOfExp) + " Experiments per cell.  Mode : No Vision")
    plt.colorbar()
    plt.show()

color_map(final_results(results , noOfExp).tolist())