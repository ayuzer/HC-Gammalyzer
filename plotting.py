"""
Plotting is a calls for plots. it can be used to make either a 3d or 
2d plot. The name 2d is actually misleading, it is used to make a 3d 
plot.
"""

import sys
import numpy as np
from PyQt4 import QtGui, QtCore
from matplotlib import cm #color mapping
import matplotlib.pyplot as plt
from mpldatacursor import datacursor #clickable annotation boxes
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import axes3d #for 3d plots
from matplotlib.ticker import AutoMinorLocator


class plotting(QtGui.QWidget):
    #for every 1D graph made , __init__, initUI , and graphRes is called.
    def __init__(self): #creation of the variables #initialized for all plotting instances
        #print('Plotting : init')
        super(plotting, self).__init__()
        self.initUI()

    def initUI(self): #initialized along with __init__
        #print('Plotting: initUI')
        self.figure=plt.figure()
        self.ax=self.figure.add_subplot(111)
        self.main_frame = QtGui.QTabWidget()
        
        
        self.canvas=FigureCanvas(self.figure)
        self.toolbar=NavigationToolbar(self.canvas,self.main_frame) #self.canvas
        self.canvas.setParent(self.main_frame) ##########
        #FigureCanvas.setPa
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.toolbar)
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        self.main_frame.setLayout(vbox)
    
    def graphRes(self, data, calib=None): 

        #print('Plotting: graphRes') #ax = figure.add_subplot(111)
        self.ax.hold(True) #plot with the same axis parameters
        if calib==None: #object warning, still works, ignore for now
            #FutureWarning: comparison to `None` will result in an elementwise object comparison in the future.
            x= np.arange(0.,len(data))          
            self.ax.plot(x,data) #regular plot if no calibration data exists

        else:
            self.ax.plot(calib, data[:len(calib)]) #if calibration exists, use calibrated x axis data (calib), and y axis as regular procssed counts (data)

        #self.dc1=datacursor(formatter="Energy:{x:.4f}\nCounts:{y:.4f}".format,bbox=None) #interactive cursor , SLOW find alternative or fix
 
        #self.ax.imshow(data, interpolation='nearest') ##ADDED
        self.ax.xaxis.set_minor_locator(AutoMinorLocator()) #auto set minor ticks
        plt.tick_params(which='both', width=1)
        plt.tick_params(which='major', length=7)
        plt.tick_params(which='minor', length=4, color='r')
        self.ax.grid(True)
        self.canvas.draw() #draw in pyQT gui canvas rather than seperate window

    def graph2DRes(self, data): #3d plot
        print('Plotting: graph2DRes..Please wait...')
        #print('data from graph2dres is: ', data)
        #############################################
        #np.savetxt('2Dcoin.csv',data ,delimiter=",")#save 2D Data as CSV for later use
        #############################################        
        
        self.ax=self.figure.add_subplot(111) #, axisbg='slategray'
        self.ax.hold(False) #dont use same axis as before 
        gridsizes=int(max(np.amax(data[:,0]),np.amax(data[:,1]))) + 100 #set grid size to max of each channel total energy 
        print('2D plot gridsize is: ', gridsizes)
        #########Gridsize not working for HEXBIN graph option below, fix############
        #make 2D total counts external message module here (factoring in min count=2)
        totalgraphicalcounts = sum(data[:,2])
        print('the total (after 2count threshold) 2D coincidence counts are: ', totalgraphicalcounts)
        ######
        print('the maximum count at a point on the 2D coincidence graph is: ', np.amax(data[:,2])) #debugging purposes

        tdcm=self.ax.hexbin(data[:,0],data[:,1],C=(data[:,2]), gridsize=gridsizes, #tdcm= two dimensional color map
            cmap= cm.nipy_spectral, bins=None) #cmap = cm.viridis -> linear color scale
         
        self.figure.colorbar(tdcm) #gradient color bar , related to above tdcm parameters
        self.ax.grid(True)
        #self.dc1=datacursor(formatter="Energy:{x:.4f}\nCounts:{y:.4f}".format,bbox=None)
           #data cursor seems to be broken for 2d Graph
        self.canvas.draw() #draw 2D color map canvas
        
  
#==============================================================================
        #triple coincidence 3D plotting work in progress
#     def graph3DRes(self, data):
#         self.ax =self.figure.add_subplot(111, projection='3d')
#         self.ax.hold(False)
#         gridsize=int(max(np.amax(data[:,0]),np.amax(data[:,1])))
#         
#         tdcm=self.ax.scatter(data[:,0],data[:,1],C=(data[:,2]), gridsize=gridsize, cmap= plt.cm.nipy_spectral_r, bins=None)
#         self.figure.colorbar(tdcm)
#         
#         self.canvas.draw()
#==============================================================================

    def newButton(self, newAction):
        print('Plotting: newButton')
        self.toolbar.addAction(newAction)
  
  