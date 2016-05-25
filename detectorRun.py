"""
The detector run class is an class that is created for all session.
It contains the processed (and if applied, calibrated) data, the raw data, the
calibration coefficients, the names of the graphs, the coincidence detections and 
the associated channels (for 2d graphs)
"""

import time
import math
import breakUp #
import plotting
import binaryRead #
import numpy as np
import peakFitting

##new for slice
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
init_notebook_mode()
##

class detectorRun():
    
    def __init__(self, fileLoc):
        print('DetectorRun: init')
        self.fileLoc=fileLoc #fileLoc = variable for file's location
        self.resInfo=[] #list/array of NAMES of resultant graphs
        self.resCalib=[] #list containing calibrated X_axis data sets (for ch 1 and ch 0/total)
        self.processed="" #processed data arrays ( 9 col array for 2 detector systems)
        self.resGraphs=[] #contains all resultant graphs
        self.matCoin=""  # matched coincidence data array (for 2D coin graph)- condensed version, obtained from parse
    
    def process(self,calib):
        print('DetectorRun: process')
        start=time.clock()
        binaryRead.binaryRead(self) #call binaryRead function to process bin data
        end=time.clock()
        
        processtime= end - start
        print("binary read processing time took %.2f (seconds)" %processtime)
        
        
        start2=time.clock()
        breakUp.breakUp(self,calib) #call breakUp function to arrange/organize processed data
        end2=time.clock()
        
        breakuptime= end2 - start2
        print('breakUp processing time took %.2f (seconds) :' %breakuptime)        
    
    def makeGraphs(self, index): #call to make graphs
        #print('DetectorRun: makeGraphs')
        y=plotting.plotting()
        x=0
        if index>2: #index = column of proccesed array (0= total, 1= total coin, 2= total ainti, 3= ch0 tot, etc)
            x=3 #set x=3 for columns of ch0, ch1 proccessed data
            
        if not self.resCalib: #if res calib is empty
            y.graphRes(self.processed[:,index]) #Calls plotting.py module to plot data
        
        else: #if calibration exists, use resCalib data
            y.graphRes(self.processed[:,index], self.resCalib[math.floor((index-x)/3)]) #return ResCalib[0] for index 0-2 (Total ch) & for index 3-5 (CH0), returns ResCalib[1] for index 6-8 (CH1)
                        
            #testdata = self.resCalib #####debugging###############
            
        self.resGraphs.append(y) #append current produced graph to resGraph list (names)
        
    def make2DGraphs(self): #called when user selects 'make 2d graph' from operations tab of  gamalyzer window
        print('DetectorRun: make2DGraph (initializing 2D Graph....)')
        y=plotting.plotting()
        y.graph2DRes(self.matCoin)#calls graph2dres from plotting.py, inputting matCoin array data
        self.resGraphs.append(y) #append to resultant graphs
#==============================================================================
#         try:#error checking
#             y.graph2DRes(self.matCoin)#calls graph2dres from plotting.py, inputting matCoin array data
#             self.resGraphs.append(y) #append to resultant graphs
#         except:
#             print('not enough meaningful 2D Coincidence data available to produce a graph' )
#             pass
#==============================================================================
        
        
    def to1And6Col(self, index): #function to save current analysis data into 1 colum and 6 column as csv files (does not output calibrated data)
        #print('DetectorRun: to1And6Col')
        print('producing 1 and 6 column csv file (non-calibrated)')   
        data=self.processed[:,index] #
        name=self.fileLoc.replace(".bin", "")
        fileBaseName=name+"_"+self.resInfo[1][index]
        output1=fileBaseName + "_1col.csv"
        output6=fileBaseName + "_6col.csv"
        with open(output1, "w") as file1, open(output6, "w") as file6:
            for i in range(len(data)):
                file1.write(str(data[i]) + "\n")
                if (i%5) == 0:
                    file6.write(str(i+1) +"," + str(data[i]) + ",")
            
                elif (i%5) == 4:
                    file6.write(str(data[i]) + "\n")
            
                else:
                    file6.write(str(data[i]) + ",")
                    
###################section for outputting calibrated csv data
    def toCalib2Col(self, index):
        
        x=0
        if index>2: #part of applying correct calib factors
            x=3
            
        if self.resCalib: #error check
            print('DetectorRun: creating calibrated 1D spectra csv data')
            xdata=self.resCalib[math.floor((index-x)/3)] # before: [math.floor((index-x)/3)]
            #print("xdata length :" ,len(xdata))
            ydatas=self.processed[:,index] #data[:len(xdata)]
            #print("ydatas length: ", len(ydatas))
            ydata= ydatas[:len(xdata)]
            name=self.fileLoc.replace(".bin", "")
            fileBaseName=name+"_"+self.resInfo[1][index] #res.Info[1][index] = Ch 1 Anti, Ch0 Coin, Total Coin, etc
            output1=fileBaseName + "_2col_calib.csv"
            with open(output1, "w") as file1:
                for i in range(len(ydata)):
                    file1.write( str(xdata[i]) + "," + str(ydata[i]) + "\n")
        else:
            print('this data set is not calibrated, cant produce calibrated csv file')
            pass

##################
    def fitPeak(self, center, index): #peak fitting function , called from peakfit def under mainwindow.py, used for manual curve fitting
        print('DetectorRun: fitPeak Method')
        x=0
        aboutCenter=center #center is the user inputed x location (i.e. 661)
        xdatas = np.arange(aboutCenter-200,aboutCenter+200)
        if index>2: #for making index 0-5 use calib factor0, and index 6-8 (ch1 datas) to use calib factor1
            x=3
        if self.resCalib: #refactoring the center point if calibration exists
            zof=self.resCalib[math.floor((index-x)/3)][0] #first value of calib factored X value, ie 0.398 (original = 1)
            fof=self.resCalib[math.floor((index-x)/3)][1]-self.resCalib[math.floor((index-x)/3)][0] #2nd value of calibrated x value - 1st (eg 0.692 - 0.398) = 0.294
            aboutCenter=int((center-zof)/fof) # eg: ((661-0.398) / 0.294) = 2246 (which is the index of uncalibrated peak location of 661 kev)
            xdatas = self.resCalib[math.floor((index-x)/3)][aboutCenter-200:aboutCenter+200]#take -200 to +200 index values from the uncalibrated center
            
        popt,pcov=peakFitting.peakFitting(self.processed[aboutCenter-200:aboutCenter+200,index])
        a,b,c,d=popt
        popt=a,b+aboutCenter-200,c,d
        xAxis=np.arange(aboutCenter-200,aboutCenter+200)
        return (xdatas,xAxis,popt)

##############################
##############################new

    def mapmatrix(self,data): #converts 3 column array into 2D mapped Matrix 
        TDMatrixArray = np.zeros( (np.amax(data[:,0])+1, np.amax(data[:,1])+1)  )
    
     #creates two-dimensional matrix array filled with 0 (mxn size is equal to max of datasets)

        for i in range(0,len(data)): #iterates from i = 0
            x = data[i,0]
            y= data[i,1]
            z= data[i,2]
            TDMatrixArray[x-1,y-1] = z #ie if x= 1 ,y=1 , then set it to the first index (0,0)
        #mapping mxn index directly to channel energy value
        return TDMatrixArray
###################################
    def makeSlicedGraph(self,lowerbound,upperbound):
        #self.matCoin exists
        TDMatrix = self.mapmatrix(self.matCoin)
        #print(len(TDMatrix))
        a = int(lowerbound)
        b = int(upperbound)
        
        RegionSlice = TDMatrix[a-1:b-1, :]
        SlicedData = RegionSlice.sum(axis=0)
        #print(SlicedData)
        graphtitle= '1D spectrum of selected region from {} to {}'.format(a,b)
        
        #graphing components below
        trace0 = Scattergl(
            y = SlicedData,                    
            mode = 'lines+markers',
            marker=dict(color='black', size=3),
            line=dict(color='rgb(84,172,234)')
            )
            
                
        data = [trace0]
        layout = dict(title = graphtitle,
            xaxis = dict(title = 'Energy', rangemode='tozero'),
            yaxis = dict(title = 'Counts',rangemode='tozero')
            )


        fig = dict(data=data, layout = layout)
        
        #change file location, and name
        name=self.fileLoc.replace(".bin","")
        newname=name+"_slicedregions_{}_to_{}.html".format(a,b)
        
        
        
        plot(fig, filename= newname)  #validify plot being saved into my destination folder
################################/end
                
        