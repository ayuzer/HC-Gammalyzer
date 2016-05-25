"""
The main window code contains the code which build the base window
as well as the tabs and sub tabs. It also maintains arrays of the 
names of the objects that have been created, both for calibration 
and analysis, as well as the objects themselves. Additionally it is 
here that additional code must be added to create more menu functions.
"""

import gc #garbage collector module
import os
import sys
import math
import time
import parse #custom
import impExp #custom
import autoNaBe #custom
import printWin #custom
import getInfWin #custom
import peakFitting #custom 
import calibration #custom
import numpy as np
import getSliceInfo

from PyQt4 import QtGui
from PyQt4 import QtCore
#################################################################

class window(QtGui.QMainWindow): 
##############################################################################    
    def __init__(self):
        super(window,self).__init__() #initiate window
        self.initUI() #intiate gui
        self.resRun=[] #resultant run data (contains everything?)
        self.resRunName=[] #result run name
        self.calibData=[] #calibration factor data contains calibration module objects (factors,factch1, peak, maxev, etc)
        self.calibName=['No Calibration Data'] 
        self.backName=[] #background data name
        self.backData=[] #background data
##############################################################################
    def initUI(self): #parameters for GUI
    
        #sys.stdout = printWin.printWin()
        #sys.stderr = printWin.printWin()
        #QtCore.QCoreApplication.processEvents 

        self.setGeometry(100, 100, 700, 600)
        self.setWindowIcon(QtGui.QIcon('web.png'))

        fileDialog = QtGui.QAction(QtGui.QIcon('10x10.png'),'Open',self)
        fileDialog.setShortcut('Ctrl+O')
        fileDialog.setStatusTip('Open and Analyze Files')
        fileDialog.triggered.connect(self.showDialog) #connect to showDialog method

        calibDialog=QtGui.QAction(QtGui.QIcon(None),'Create Calibration File', self)
        calibDialog.setShortcut('Ctrl+I')
        calibDialog.setStatusTip('Create Calibration File')
        calibDialog.triggered.connect(self.makeCalib)

        recoverCalib=QtGui.QAction(QtGui.QIcon(None),'Load Calibration File', self)
        recoverCalib.setShortcut('Ctrl+l')
        recoverCalib.setStatusTip('Load Calibration Data')
        recoverCalib.triggered.connect(self.loadCalib)

        loadDataAnalysis=QtGui.QAction(QtGui.QIcon(None),'Load Analysis Session', self)
        loadDataAnalysis.setShortcut('Ctrl+N')
        loadDataAnalysis.setStatusTip('Load Calibration Data')
        loadDataAnalysis.triggered.connect(self.loadAnalysis)

        exitAction=QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.close) #self.close

        garbCol=QtGui.QAction('Cleanup Memory', self)
        garbCol.setStatusTip('Cleanup Memory')
        garbCol.triggered.connect(self.collectGarb)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(fileDialog)
        fileMenu.addAction(garbCol)
        fileMenu.addAction(calibDialog)
        fileMenu.addAction(recoverCalib)
        fileMenu.addAction(loadDataAnalysis)
        fileMenu.addAction(exitAction)

        backgroundFile=QtGui.QAction(QtGui.QIcon(None),'Load Background File', self)
        backgroundFile.setShortcut('Ctrl+b')
        backgroundFile.setStatusTip('Load Background Data')
        backgroundFile.triggered.connect(self.createBack)

        backgroundLoad=QtGui.QAction(QtGui.QIcon(None),'Load Analysis File as Background', self)
        backgroundLoad.setShortcut('Ctrl+y')
        backgroundLoad.setStatusTip('Load Background Data From Analysis File')
        backgroundLoad.triggered.connect(self.loadBack)

        backgroundSub=QtGui.QAction(QtGui.QIcon(None),'Apply Background to Current Data Set', self)
        backgroundSub.setShortcut('Ctrl+t')
        backgroundSub.setStatusTip('Subtract Background Data')
        backgroundSub.triggered.connect(self.subBack)

        make2DGraph=QtGui.QAction(QtGui.QIcon(None),'Make 2-D Coincidence\nGraph for Current Dataset', self)
        make2DGraph.setShortcut('Ctrl+j')
        make2DGraph.setStatusTip('Make 2-D Coincidence Graph')
        make2DGraph.triggered.connect(self.make2DGraph)
        
        ########new for sliced2dgraph
        slice2Dcoin=QtGui.QAction(QtGui.QIcon(None),'Slice 2-D Coincidence\nGraph for Current Dataset', self)
        slice2Dcoin.setShortcut('Ctrl+x')
        slice2Dcoin.setStatusTip('Slice a region from 2-D Coincidence Graph and display 1D spectrum')
        slice2Dcoin.triggered.connect(self.slice2Dcoin)
        #############################

        printInfo=QtGui.QAction(QtGui.QIcon(None),'Print Info', self)
        printInfo.setStatusTip('Print Info for Current Dataset')
        printInfo.triggered.connect(self.printInfo)

        autoNaBe=QtGui.QAction(QtGui.QIcon(None),'Determine Na-22 and Be-7 Concentrations', self)
        autoNaBe.setStatusTip('Find Na-22 and Be-7 Concentrations in Selected Samples')
        autoNaBe.triggered.connect(self.findNaBe)

        
        operationMenu = menubar.addMenu('&Operations')
        operationMenu.addAction(make2DGraph)
        operationMenu.addAction(slice2Dcoin) ##new
        operationMenu.addAction(backgroundFile)
        operationMenu.addAction(backgroundLoad)
        operationMenu.addAction(backgroundSub)
        operationMenu.addAction(printInfo)
        operationMenu.addAction(autoNaBe)
        
        ####for about window
        aboutAction= QtGui.QAction(QtGui.QIcon(None), '&About', self)
        aboutAction.triggered.connect(self.about)
        
        AboutMenu = menubar.addMenu('&help')
        AboutMenu.addAction(aboutAction)
        #####

        self.exp=QtGui.QTabWidget() #setting shortcut for Qtabwidget module (used alot in this class)
        self.exp.setTabsClosable(True)
        self.exp.tabCloseRequested.connect(self.tabKill)
        self.setCentralWidget(self.exp)

        self.statusBar().showMessage('Ready')

        self.resize(500,500)
        self.center()

        self.setWindowTitle('Gammalyzer')

        self.show()
  
##############################################################################
    def about(self):
       QtGui.QMessageBox.about(QtGui.QWidget(),'About',
       "Version 1.0 Created by Aaaron English (Winter 2015), modified by Maverick Mailhot \nVersion 1.5 created by James Ro (Winter 2016)")
###############################################################################
    #prints out in cmdline current file location, calibrated X_values, total sum of counts for each subtab, and the array itself
    def printInfo(self): #works, but needs to make it look nicer
        print(self.resRun[self.exp.currentIndex()].fileLoc) #prints current data location
        for idx, data in enumerate(self.resRun[self.exp.currentIndex()].resInfo[0]):
            print(data,': ',self.resRun[self.exp.currentIndex()].resCalib[idx])

        for idx, data in enumerate(self.resRun[self.exp.currentIndex()].resInfo[1]):
            if idx<len(self.resRun[self.exp.currentIndex()].processed[0]):
                print(data,': ',np.sum(self.resRun[self.exp.currentIndex()].processed[:,idx]),
                    self.resRun[self.exp.currentIndex()].processed[:,idx]) 
     
###############################################################################
     
    def closeEvent(self, event): 
        reply=QtGui.QMessageBox.question(self,'Message',"Are you sure you want to quit?",
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()

        else:
            event.ignore()
   
###############################################################################
    def center(self): #centers window when program is initiated
        qr=self.frameGeometry()
        cp=QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
  
###############################################################################
    def collectGarb(self):
        remaining=gc.collect()
        print(remaining) 
  
###############################################################################
    def checkCalib(self): #check if calibration file exists, called when opening a file
        fileName = QtGui.QFileDialog.getOpenFileNames(self,'Open file','/home')
        ok=False
        if fileName:
            calib, ok=QtGui.QInputDialog.getItem(self,'Which Calibration Sould be Used?',
                'Select...',self.calibName,current=0,editable=False)
            if ok:
                if calib==self.calibName[0]: # [0] index is no calibration file
                    calib=None

                else: #else,go through calibName index to select valid calibration
                    for idx, cali in enumerate(self.calibName):
                        if calib==cali:
                            #print('mainwindow.py :def checkcalib: calib, calibData ', calib, self.calibData[idx-1]) #calib = calib name, calibData = calibbration.calibration object
                            calib=self.calibData[idx-1] #this links the calibration object, which also includes calib.factors
                            #print('mainwindow.py :def checkcalib: calib.factors ',calib.factors)
                            break

                ok=True #return ok=true if valid calibration file is selected

        return(ok,fileName,calib) 
  
##############################################################################
  
    def showDialog(self): #called from opening a file , initates parse.py and in term detectorrun.py using calib as the inherited variable
        ok,fileName,calib=self.checkCalib() #call calibration check method above
        if ok: #ok is set to true even if None calib was chosen
          x=parse.parse(fileName, calib) #sets x to run parse function to grab graphs to display
          self.displayGraphs(x) #initiates display graphs below
    
##############################################################################
    
    def displayGraphs(self, x): #creates graphs through plottings function (total, ch1, ch0, regular + coincidence + anticoincidence)             
      
        print('Plotting graphs...')        
        for i in x: #x is list containing detectorRun objects, i is the first object instance (usually the only one)
            for j in range(0, i.processed.shape[1]): #for each column of processed
                i.makeGraphs(j) #calls makeGraph function from DetectorRun Module
                #pass

            self.subTabs=QtGui.QTabWidget()
            self.subTabs.setTabsClosable(True)
            self.subTabs.tabCloseRequested.connect(self.tabKill)
            names=i.resInfo[1]  #names of graph (ie Tot Coin)
            
            make1And6Col=QtGui.QAction(QtGui.QIcon('exit.png'),'Make Files',self)
            make1And6Col.setShortcut('Ctrl+f')
            make1And6Col.triggered.connect(lambda: self.resRun[self.exp.currentIndex()
                ].to1And6Col(self.exp.currentWidget().currentIndex()))
                
            ###new calibrated 1D spectra data array creation 
            makeCalib2Col=QtGui.QAction(QtGui.QIcon('calibrationicon.png'),'Make Calibrated csv data file',self)
            makeCalib2Col.setShortcut('Ctrl+x')
            makeCalib2Col.triggered.connect(lambda: self.resRun[self.exp.currentIndex() #self.exp=QtGui.QTabWidget()
                ].toCalib2Col(self.exp.currentWidget().currentIndex()))                
           

            fitPeak=QtGui.QAction(QtGui.QIcon('Gaussian_distribution.png'),'Fit Gauss Function (+ find area)',self)
            fitPeak.triggered.connect(lambda: self.fitPeak(self.exp.currentIndex()
                ,self.exp.currentWidget().currentIndex())) 
                
            for idx, k in enumerate(i.resGraphs): #iterates through sequence, returning a tuple of count # and the value of the current sequence
                name=names[idx] #idx = counter, k = element value (current graph object data in this case)
                self.subTabs.addTab(k.main_frame, name)#####k.canvas
                k.toolbar.addAction(make1And6Col)
                k.toolbar.addAction(makeCalib2Col) #new section added
                k.toolbar.addAction(fitPeak)
                #self.exp=QtGui.QTabWidget()
            self.exp.addTab(self.subTabs, i.fileLoc) #in current analysis seesion, add subtabs for each graph type (tot, ch0, ch1, etc)
            self.resRunName.append(i.fileLoc)

        self.resRun.extend(x) #extends the list with contents of x sequence (resRun list is appended here)
        print('done plotting')


        #testdata2 = self.resRun ####DEBUGGING####
##############################################################################
  
    def subBack(self): #subtract background data from current data set, prompts to use a loaded background, then proceeds to plot new graphs with background data subtracted from current data
        #'apply background to current data plot'        
        back, ok=QtGui.QInputDialog.getItem(self,'Which Background file Sould be Used?',
            'Select...',self.backName,current=0,editable=False)

        if ok:
            for idx, background in enumerate(self.backName):
                if background==back:
                    back=self.backData[idx]
                    break

            x=parse.parseBackSub(back,self.resRun[self.exp.currentIndex()])
            self.displayGraphs(x) 
##############################################################################
   
    def createBack(self): #create background file , prompts to open a bin file, then loads it as background file for later use
        #'load background file'        
        ok,fileName,calib=self.checkCalib()
        if ok:
          x=parse.parse(fileName, calib)
          self.backData.extend(x)
          self.backName.extend(fileName)
          print(self.backData, self.backName)

##############################################################################

    def loadBack(self): #load analysis (.anze) file as background
        fileName=QtGui.QFileDialog.getOpenFileNames(self,'Open .anze file','/home')
        if fileName:
          x=impExp.loadFromFile(fileName)
          self.backData.extend(x)
          self.backName.extend(fileName)
##############################################################################
    
    def fitPeak(self, superInd, subInd): #user inputted peak fitting, for fitting gaussian curve into graphs, as well as displaying the area + FWHM
        center, ok=QtGui.QInputDialog.getDouble(self, 'Enter the Estimated Center of the Gaussian Function', 'Enter...')
        if ok:
            xCal,xTrue,popt=self.resRun[superInd].fitPeak(center, subInd) #calls fitPeak module from DetectorRun.py
            #print(xCal,xTrue,popt) #x cal = calibrated x values, xTrue = xAxis=np.arange(aboutCenter-200,aboutCenter+200)
            self.resRun[superInd].resGraphs[subInd].ax.plot(xCal, peakFitting.gauss_function(xTrue,*popt), 'r') #calls peakFitting.py's gaussian function, then plots
            a,b,c,d=popt #a=amplitude,b=center, c=std deviation
            
            factor = xCal[2]-xCal[1] #find calibration factor by subtracting 2nd energy point by first
            
            AreaInfo = (a*abs(c)*math.sqrt(math.pi)) * factor #integral equation of arbitrary gaussian function 
            FWHM = 2.*c*math.sqrt(2.*math.log(2.)) * factor #FWHM calcuation
            print('Area: %f' % (AreaInfo) ) #area under the fitted gaussian curve 
            print('FWHM: %f' %(FWHM))
            print('Peak center: %f' %(b*factor+factor)) #center of fitted peak
            
            #Todo: add the above print info into the designated plot as an annotation
            self.resRun[superInd].resGraphs[subInd].canvas.draw() #draw fitted curve on current tabs canvas (renamed to main_frame)
##############################################################################
   
    def make2DGraph(self): #function to call 2D graph
        x=self.resRun[self.exp.currentIndex()] #(self.exp = QtabWidget, current tab)
        
        if x.matCoin.size: #check if  2D array exists
            x.make2DGraphs() #calls make2dGraphs function from DetectorRun
            name=x.resInfo[-1][-1] #get name of graph eg) 2D Coincidence from resInfo name array list
            self.exp.currentWidget().addTab(x.resGraphs[-1].main_frame, name) #add 2d graph tab inside the main window
        else:
            print('not enough meaningful 2D Coincidence data available to produce a graph' )
##############################################################################
    def slice2Dcoin(self):
        x= self.resRun[self.exp.currentIndex()]
        if x.matCoin.size:
            lowerbound, upperbound, ok=getSliceInfo.getSliceInfo.getSlice(self)
            if ok:
                #filename= x.fileLoc#
                x.makeSlicedGraph(lowerbound, upperbound)
        else:
            print('not enough meaningful 2D Coincidence data available to slice a graph' )
##############################################################################
  
    def makeCalib(self): #function to call calibration module, using getInfWin to collect user input
        detectorName, maxEv, peaks, ok=getInfWin.getInfWin.getInf(self)
        if ok:
            fileName=QtGui.QFileDialog.getOpenFileName(self,'Open file','/home') #prompts open file explorer for user to select file
            calRes=calibration.calibration(fileName,detectorName) #call calibration object
            calRes.peak=peaks
            calRes.maxEv=float(maxEv)
            calRes.process() 
            impExp.saveToFile(calRes, calRes.fileLoc.replace(".bin",".gaze")) #using pickle, saves calibrated data (calRes) as .gaze file
            self.calibData.append(calRes)
            self.calibName.append(calRes.detName)
##############################################################################
   
    def loadCalib(self):
        fileName=QtGui.QFileDialog.getOpenFileNames(self,'Open .gaze file','/home')
        x=impExp.loadFromFile(fileName)
        self.calibData.extend(x)
        for i in x:
            self.calibName.append(i.detName)
##############################################################################
   
    def loadAnalysis(self):
        fileName=QtGui.QFileDialog.getOpenFileNames(self,'Open .anze file','/home')
        x=impExp.loadFromFile(fileName)
        self.displayGraphs(x)
##############################################################################
  
    def tabKill(self,index):
        sender=self.sender()
        reply=QtGui.QMessageBox.question(self,'Closing Tab',
            "Are you sure you want to Close This Tab? All data within will be deleted",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if reply==QtGui.QMessageBox.Yes:
            if sender is self.exp:
                del self.resRun[index]
                self.exp.removeTab(index)

            else:
                self.resRun[self.exp.currentIndex()].processed=np.delete(
                    self.resRun[self.exp.currentIndex()].processed, [index], axis=1)
                del self.resRun[self.exp.currentIndex()].resInfo[1][index]
                self.exp.currentWidget().removeTab(index)
##############################################################################
                
    def findNaBe(self): #not working as of moment, calls autoNaBe class objects
        naBe=autoNaBe.autoNaBe(self.backName,self.resRunName)
        result=naBe.exec_()
  
##############################################################################
  
  