"""
Parse is the intermediary between the detectorRun class and 
mainwindow. parse takes care of background subtraction and 
the regular processing (with or without the calibration)

Creates ResCalib (which contains calibrated x_axis data for  energy)
"""
import time
import math
import copy
import impExp #
import numpy as np
import detectorRun #

###############################################################################
def parse(fileName, calib):
    #print('Parse module has been called')
    print('Processing data..please wait..(expect 1min load time per 150k events)')
    x=[]
    for i in fileName: #not sure why this is in a for loop if filename is just 1 element, perhaps because filename is a list 
        #print(' file name in parse: ', fileName) #debug
        x.append(detectorRun.detectorRun(i))
        x[-1].process(calib)
        if calib!=None: #if calib isnt the default 'none', aka calibration exists
            print('applying calibration factor to data.. please wait..')
            for j in range(0, len(x[-1].resInfo[0])): #range in calib lists (eg: len[1,2 = 2]), for making 2 calibrated x_axis sets , eg) x[-1].resInfo[0] = [2,1]
                x[-1].resCalib.append(np.arange(calib.factors[j][1], calib.maxEv+calib.factors[j][1],calib.factors[j][0]) ) 
                #creating facotred datas for X axis (0 intercept to max energy , in steps of calib factor value) (populates resCalib list in detRun module)
                try: #factoring 2D coincidence data with calibration               
                    x[-1].matCoin[:,j]=(x[-1].matCoin[:,j]*calib.factors[j][0])+calib.factors[j][1] 
                except: #exception error if 2d coin matrix has no coincidences
                    print('2D coincidence array has no data, skipping calibration factor application')
                    pass 
                #print('def parse: x[-1].resCalib[j] value is: ', x[-1].resCalib[j])
                
            name=x[-1].fileLoc.replace(".bin", "-calibrated.anze")
            impExp.saveToFile(x[-1], name) #pickle calibrated data and save for easy loading in the future
        else:
            name=x[-1].fileLoc.replace(".bin", ".anze")
            impExp.saveToFile(x[-1], name) #pickle non-calibrated data and save for easy loading in the future

            #y=0
   
    #print('made it through - parse')
    return x #x contains the detectorRun objects
 
###############################################################################
    
def parseBackSub(back,data): #called from mainwindow,subtract background data from current data set
    x=[]
    name=data.fileLoc.replace('.bin', '-backgroundremoved.bin')
    x.append(detectorRun.detectorRun(name))
    x[-1].resInfo=copy.copy(data.resInfo)
    x[-1].resCalib=copy.copy(data.resCalib)
    x[-1].matCoin=np.copy(data.matCoin, order='C')
    if len(data.processed[:,0])<len(back.processed[:,0]):
        x[-1].processed=data.processed-back.processed[0:len(data.processed[:,0]),:]
        
    else:
        x[-1].processed=data.processed[0:len(back.processed[:,0]),:]-back.processed

    x[-1].processed=x[-1].processed.clip(min=0)
    z=0
    y=0
    matCoinEnd=0
    if len(data.matCoin[:,0])<len(back.matCoin[:,0]):
        matCoinEnd=len(data.matCoin[:,0])
        
    else:
        matCoinEnd=len(back.matCoin[:,0])
    
    while z+1<matCoinEnd:
        while y+1<matCoinEnd and data.matCoin[z,0]>=back.matCoin[y,0]:
            if data.matCoin[z,0]==back.matCoin[y,0] and data.matCoin[z,1]==back.matCoin[y,1]:
                x[-1].matCoin[z,2]=data.matCoin[z,2]-back.matCoin[y,2]
                if x[-1].matCoin[z,2]<0:
                    x[-1].matCoin[z,2]=0
                    
                break
            
            y+=1
            
        z+=1
        y=0
        if z>600:
            y=z-500
        
    print(x[-1].fileLoc)
    name=x[-1].fileLoc.replace(".bin", ".anze")
    impExp.saveToFile(x[-1], name)
    return x
 
 ###############################################################################