"""
Code used to get regions to slice
"""

from PyQt4 import QtGui
from PyQt4 import QtCore

class getInfWin2(QtGui.QDialog):
	def __init__(self, parent=None):

		super(getInfWin2, self).__init__(parent)

		self.formLayout=QtGui.QFormLayout()
		
		self.lowerbound=QtGui.QLineEdit(self)
		self.upperbound=QtGui.QLineEdit(self)
		
		self.formLayout.addRow("lower bound cut:", self.lowerbound)
		self.formLayout.addRow("upper bound to cut:", self.upperbound)
		
		self.buttons=QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.ActionRole |
			QtGui.QDialogButtonBox.ResetRole | QtGui.QDialogButtonBox.Ok | 
			QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal,self)
		
		self.buttons.addButton(self.mpButton,QtGui.QDialogButtonBox.ActionRole)
		self.buttons.addButton(self.rButton,QtGui.QDialogButtonBox.ResetRole)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
		self.formLayout.addRow(self.buttons)
	
		self.setLayout(self.formLayout)
	
		
	def getInfo(parent=None): #called from mainWindow module (for collecting user input calibration parameters)
		dialog=getInfWin2(parent)
		result=dialog.exec_()
		
		lowerbound = max( 0., float( dialog.lowerbound.text() ) )
		
		return(lowerbound, float(dialog.upperbound.text()),result)


#########################to put into mainwindow.py
operationMenu.addAction(slice2Dcoin)

	def slice2Dcoin(self):
		lowerbound, upperbound, ok=getInfWin2.getInfWin2.getInfo(self)
		if ok:
			x= self.resRun[self.exp.currentIndex()]
			#filename= x.fileLoc#
			x.makeSlicedGraph(lowerbound, upperbound)
			
###########################to put into detectorRun.py
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot
from plotly.graph_objs import *
init_notebook_mode()
			
	def makeSlicedGraph(lowerbound,upperbound):
		TDMatrix = mapmatrix(self.matCoin)
		a = lowerbound
		b = upperbound
		
		RegionSlice = TDMatrix[a-1:b-1, :]
		SlicedData = RegionSlice.sum(axis=0)
		
		shortxlist = np.ma.nonzero(SlicedData)  #list with all the 0 entries removed
		shortylist = []

		for i in shortxlist[0]:
			shortylist.append(SlicedData[i])
			
		#graphing below
		trace0 = Scattergl(
			x = shortxlist[0],                 #np.arange(0, len(SlicedData)),
			y = shortylist,                            #SlicedData,
			mode = 'lines+markers',
			marker=dict(color='black', size=3),
			line=dict(color='rgb(84,172,234)')
			)


		data = [trace0]

		layout = dict(title = '1D Spectra of selected region',
			xaxis = dict(title = 'Energy', rangemode='tozero'),
			yaxis = dict(title = 'Counts',rangemode='tozero')
			)


		fig = dict(data=data, layout = layout)
		
		#change file location, and name
		name=self.fileLoc.replace(".bin","")
		newname=name+"_slicedregions_{}_to_{}.html".format(lowerbound,upperbound) #validify
		
		
		
		plot(fig, filename= newname)
			
				
###########################put into detectorRun.py
	def mapmatrix(data): #converts 3 column array into 2D mapped Matrix 
		TDMatrixArray = np.zeros( (np.amax(data[:,0])+1, np.amax(data[:,1])+1)  )
    
     #creates two-dimensional matrix array filled with 0 (mxn size is equal to max of datasets)

		for i in range(0,len(data)): #iterates from i = 0
			x = data[i,0]
			y= data[i,1]
			z= data[i,2]
			TDMatrixArray[x-1,y-1] = z #ie if x= 1 ,y=1 , then set it to the first index (0,0)
        #mapping mxn index directly to channel energy value
		return TDMatrixArray


				
		