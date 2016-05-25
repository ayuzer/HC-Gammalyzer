"""
simpleBreak is a shortened version of breakUp which is used for doing calibration
arrays. because the calibration only needs the totals for each channel, the rest
of the array can be ignored and not made. this shortents the processing time
and reduces the memory consumed for this operation
"""

import numpy as np
from random import randint

def simpleBreak(det):
	size = det.res.shape[0]
	chan=det.resInfo[0]
	processed=np.zeros((np.nanmax(det.res[:,4])+1,(len(chan))), dtype=np.int) #create 2D array rows from det.res and channels as columns
	for i in range(0, size):
		randValue=((randint(1,2)*2)-3)/10 #results in random value of 0.1 or -0.1
		energy=int(round((det.res[i,4]/2)-randValue)) #rounding off the energy values using above
		if(energy>5):
			k=0
			for j in range(0, len(chan)):
				if det.res[i,0]==chan[j]:
					k=j #this is section in general is confusing to understand..
	
			processed[energy,k]+=1 #adding a count value to the appropriate index container
	
	det.processed=processed