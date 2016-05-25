"""
calibration is a class that provides the framework for doing calibrations.
It creates a class that holds a max energy limit, the peaks found (dependant on user)
and finally the factors calculated to apply to the data the would follow.
"""

import binaryRead
import detectorRun
import simpleBreak
import peakFitting
import numpy as np
from scipy import stats

class calibration(detectorRun.detectorRun): #inheritance from detector run object
    
    def __init__(self, fileLoc, detName):
        print('Calibration : initiating objects')
        self.detName=detName #calibration detector name (from user input infwin.py)
        self.maxEv=5000. #default value of max Ev
        self.peak=[] #list of user inputted peak values
        self.factors=[] #factor data from linregress (Total and Ch0 factor)
        self.factChTo1=[] #Ch1 factor
        super(calibration,self).__init__(fileLoc) #grabbing fileLoc from outside class
    
    def process(self): #reads from binary for calibration processing, uses simple break for ch total only
        print('Calibration : Process')
        binaryRead.binaryRead(self)
        simpleBreak.simpleBreak(self)
        self.findPeakandFit() 
    
    def findPeakandFit(self): #Calibration calculations happen here
        print('Calibration : findPeakandFit')
        #self.peak.sort() #sorts user inputted peaks from lowest kev to highest kev
        for i in range(0,self.processed.shape[1]): #looping for each channel
            ##maxtemp=[] #was called max originally, took it out since it wasnt being used
            maxLoc=[] # gaussian curve fitting adjusted peak locations (using user desired known peaks)

            chanTot=self.processed[:,i] #grabs all rows for the i'th channel (total data for 1: combined total, 2: ch 0 total, 3: ch 1 total
            #baseline=1.2*np.average(chanTot) #not used,commented out
            for j in self.peak: #for each value of user inputted peaks, goes 1 at a time, from lowest Kev to highest Kev peak
                upLim=100 #originally 200
                lowLim=100 #originally 200
                maxPos=np.argmax(chanTot) #returns [index] of the maximum value element(highest counted) in current channel data (to match user peak with datas highest counted peak)
                if maxPos<100: #if the highest counted peak is located within the 1st 100 indices, disregard them
                    chanTot[0:100]=0
                    
                maxPos=np.argmax(chanTot)
                # while chanTot[maxPos+upLim]>baseline and  and maxPos+(upLim+1)<chanTot.shape:
                    # upLim+=1
                # while chanTot[maxPos-lowLim]>baseline and maxPos-(lowLim+1)>0:
                    # lowLim+=1
                #print(baseline, maxPos+upLim, maxPos-lowLim) 
                ##maxtemp.append(list(chanTot[maxPos-lowLim:maxPos+upLim+1])) #add values to maxtemp, add the max counts, took out since its unused
    
                popt,pcov=peakFitting.peakFitting(chanTot[maxPos-lowLim:maxPos+upLim]) #curve fits the region of interest (current peak +/- lims)
                a,b,c,d=popt #returns optimal values for gaussian function [ a* exp-(x-b)^2 / 2c^2) ] where a =height, b = center position, c= sigma (width)
                #print(' gaussian fitted center index (b) vs argmax center index: ' ,b,maxPos) #debugging
                ######################check validity of below line
                maxLoc.append(b+maxPos-lowLim) #########adjusted max location index
                #######################/end check
                chanTot[maxPos-lowLim:maxPos+upLim]=0 #setting the values around the adjusted max location to equal 0, getttng rid of noise, also to move onto next high peak
            
            if i==0: #if the detector channel is 0
                ch1MaxLoc=maxLoc #then causes linear regression to equal 1 (no change)
            
            else: #if doing calibration on detector channel 1 now
                fact=stats.linregress(maxLoc,ch1MaxLoc)  #find the linear regression between ch1 adjusted peak and ch0 adjusted peaks 
                self.factChTo1.append(list(fact)) #ch alignment regression results (returns a,b,c,d,e : slope,intercept,rvalue,pvalue,sterr)
                
            maxLoc.sort()
            userpeak = self.peak[:]
            userpeak.sort()
            
            fact=stats.linregress(maxLoc,userpeak) #this is the actual calibration factor between user desired Kev peaks and raw data energies
            self.factors.append(list(fact))
        print('Total and Ch0 Calibration factor: ',self.factors)
        print("Ch1 Calibration factor: ", self.factChTo1)
        
        
        
        
'''
How calibration process works:

Given user inputted peaks, 
Input Conditions: 
1) need to be highest counted peaks, not highest energy peaks
2) inputted peaks have to be relatively spaced apart (ie, no 59.5 and 46.5kev peaks to be used together , current min threshold set to 100 index ranges around the desired peak location)
3) no peaks with low KeV values (current threshold is set to disregard peaks that are within 100 INDEX location of data)
---------------------------------------------------
Example of Valid peak input (for Sample X01729):  [59.5, 661.7, 1173.2, 1332.5]
---------------------------------------------------
Calculation Process:
1) run through user inputted peaks in order
2) finds index location of highest counted value, disregards the value if index location is <100
3) grabs -100 to +100 region around the chose index, then performs gaussian peak fitting to find curve fitted center of peak
4)after appending the center peak, sets surround area (-100:+100) to be 0
5) Repeat step 1-4 until all desired peaks are calculated

6)find calibration factor by performing linear regression between data peaks and user desired peaks locations
7)performs linear regression between channel (0 & 1) to find best average calibration
'''        
          
