"""
breakUp follows immediately after binaryRead and 
takes in the array created from the binary file and
separates it into an array that follows the pattern 
[0]all detections combined, [1]all coincidence detections combined,
[2]all anticoincidence detections combined, [3]ch1 tot, [4]ch1 coin, [5]ch1 anti,
[6]ch2 tot...,[7], [8] etc. in that fashion. 
it also creates an array of the names of the plots with the channels
and an array of the channels used
"""

import numpy as np
from random import randint

def breakUp(det,calib):
    print('breakup processing...Please wait...')
    size = det.res.shape[0] #total rows 
    chan=det.resInfo[0] #current channels (1 by 2 array)
    plotsMade=[] #contains index 0-9 (10 total), look at above for naming convention  <-- for 2 channel data
    plotsMade.append("Total")
    plotsMade.append("Tot Coin")
    plotsMade.append("Tot Anti")
    ################################
    minEng=1 # minimum CH energy cut off (filters low channel energy data)
    ################################
    for i in range(0,(3*len(chan))): #where the plot names are created
        x=int(1 + ((i-3)/3) )
        if (i-3*x)==0:
            plotsMade.append("Ch "+str(x)+" Tot")
        elif (i-3*x)==1:
            plotsMade.append("Ch "+str(x)+" Coin")
        elif (i-3*x)==2:
            plotsMade.append("Ch "+str(x)+" Anti")

    plotsMade.append("2D Coincidence")
    det.resInfo.append(list(plotsMade)) #resInfo is the array containing NAMES of plots
    processed=np.zeros(  ( (np.nanmax(det.res[:,4])+1), (3+3*len(chan)) ) , dtype=np.int) #contains all array (9 column) , nanmax returns largest value within array
    matCoin=np.zeros((size,2), dtype=np.int)    
    lastCounted=1
    for i in range(0, size):
        randValue=((randint(1,2)*2)-3)/10 #creates 0.1 or -0.1 value
        energy=int(round((det.res[i,4]/2)-randValue)) #using above value for random rounding to counteract the division of energy
        enTot=energy
        coin=det.res[i,5] #coincidence (true, false) condition from binary read
        if(energy>minEng):
            
            k=0
            for j in range(0, len(chan)):
                if det.res[i,0]==chan[j]:
                    k=j+1
            
            if k>1 and calib: #only if calib exists
                enTot=int((energy*calib.factChTo1[k-2][0]) +calib.factChTo1[k-2][1])  #highest factored energy value
                
            processed[enTot,0]+=1    #for combined total channels graph
            processed[energy,3*k]+=1 #for single channel total
            if coin:
                processed[energy,(1+(3*k))]+=1 #for creating coincidence graph of each channel (ch0 coin, ch1 coin)
                processed[enTot,1]+=1 #for combined channels coincidence (total coincidence)
                
                ##section for preparing 2D coincidence array (matCoin)
                if lastCounted and det.res[i+1,5]: #if last counted and det.res's coincidence boolean value is 1 (true)
                    matCoin[i,0]=energy #filling up matched coincidence array with value (for column 1)
                    randValue=((randint(1,2)*2)-3)/10 #creates 0.1 or -0.1 value
                    energy2=int(round((det.res[i+1,4]/2)-randValue)) #using above value for random rounding to counteract the division of energy
                    matCoin[i,1]=energy2 #matched coincidence array, for colum 2 (col 1 = ch 0, col 2 = ch 1)
                    lastCounted=0 
                
                else:
                    lastCounted=1
                ##end matCoin section
    
            else:
                processed[energy,(2+(3*k))]+=1 #individual channel anticoincidence append (ch0 anti, ch1 anti)
                processed[enTot,2]+=1 #combined channel anticoin append (total anti)

    det.processed=processed #this array has 9 columns (data for all detector combinations except for 2D Coincidence)
    
 #section below is for 2D coincidence list creation, where we are masking out values that have 0 values
    matMask=np.ma.mask_rows(np.ma.masked_where(matCoin<1,matCoin,copy=True)) #masking all 0 element entries in matCoin array
    xCond=matMask[:,0].compressed() #compress(truncates invalid masked entries) -> creates 1d array (contains all CH0 coincidences)
    yCond=matMask[:,1].compressed() # Contains all CH1 Coincidences
    matCoinOrd=np.lexsort((yCond,xCond)) #lexsorted array by xCond , then by yCond values (returns the sorted values of the INDEX ), sorts from lowest to highest
    z=0
    condensed=[] #contains the 2D coincidence array (current settings have minimum count threshold to be 2)
    for i in range(0,matCoinOrd.size): #creates the 2D coincidence array from matCoin prelimary array, z = count that will increase for each coincidence hit
        z+=1
        ############below (z>1) means count threshold is 2 (atleast 2 counts need to be registed per point to be counted##########
        if(z>1 and (yCond[matCoinOrd[i]]!=yCond[matCoinOrd[i+1]] # if value of first sorted index and subsequent does not equal each other , for both x or y, basically if count doesnt have a repeat
                or xCond[matCoinOrd[i]]!=xCond[matCoinOrd[i+1]])):
            condensed.append((xCond[matCoinOrd[i]],yCond[matCoinOrd[i]],z)) #append to condensed 2D coin list (CH0 energy, Ch1 energy, counts=1)
            z=0 #reset count
       
       #z<2 means if z has to be 1, the above and below if/elif statements, essentially only append to 2D coin graph if the count is atleast 2 per x,y coordinate grid 
        elif(i+1>=matCoinOrd.size or (z<2 and (yCond[matCoinOrd[i]]!=yCond[matCoinOrd[i+1]] #end when counter is 1 below end of index. or when z is less than 2 and no more coincidences occur
                or xCond[matCoinOrd[i]]!=xCond[matCoinOrd[i+1]]))):
            z=0 #reset z to 0 when above conditions met #gets rid of coincidence counts that are less than 2

    condCoin=np.array(condensed)
    #print('conCoin(aka matCoin) array is', condCoin) #debugging purposes, save this data
    print('the total number of 2D coincidence counts are: ', len(yCond)) #save this data to view as log in MainWindow.py
    det.matCoin=condCoin