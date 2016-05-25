"""
This code creates a class that when called creates a window that
is used to input the values necessary to carrying out a 
calibration. 
"""

from PyQt4 import QtGui
from PyQt4 import QtCore

class getInfWin(QtGui.QDialog):
	def __init__(self, parent=None):

		super(getInfWin, self).__init__(parent)

		self.formLayout=QtGui.QFormLayout()
		
		self.detectorName=QtGui.QLineEdit(self)
		self.maxEv=QtGui.QLineEdit(self)
		self.peaks=[]
		self.peaks.append(QtGui.QLineEdit(self))
		
		self.formLayout.addRow("Detector Name:", self.detectorName)
		self.formLayout.addRow("Max Energy to Show(keV):\n(Default 5000 keV)", self.maxEv) #maximum peak value to show on graph
		self.formLayout.addRow("Highest Peak (keV)", self.peaks[0])
		
		self.mpButton = QtGui.QPushButton('More Peaks', self)
		self.mpButton.clicked.connect(self.addPeakLoc)
		
		self.rButton = QtGui.QPushButton('Reset', self)
		self.rButton.clicked.connect(self.reset)
		
		self.buttons=QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.ActionRole |
			QtGui.QDialogButtonBox.ResetRole | QtGui.QDialogButtonBox.Ok | 
			QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal,self)
		
		self.buttons.addButton(self.mpButton,QtGui.QDialogButtonBox.ActionRole)
		self.buttons.addButton(self.rButton,QtGui.QDialogButtonBox.ResetRole)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
		self.formLayout.addRow(self.buttons)
	
		self.setLayout(self.formLayout)
	
	def addPeakLoc(self):
		self.peaks.append(QtGui.QLineEdit(self))
		self.formLayout.addRow("Next Highest Peak (keV)", self.peaks[-1])
		self.formLayout.addRow(self.buttons)
		self.setLayout(self.formLayout)
		
	def reset(self):
		print("self.peaks is ",self.peaks)
		if len(self.peaks)>1:
			for i in range(0,len(self.peaks)-1):
				print(i)
				label=self.formLayout.labelForField(self.peaks[-1])
				if label is not None:
					label.deleteLater()
				
				self.peaks[-1].deleteLater()
				del self.peaks[-1]
	
	def getInf(parent=None): #called from mainWindow module (for collecting user input calibration parameters)
		dialog=getInfWin(parent)
		result=dialog.exec_()
		peakSend=[] #
		for i in dialog.peaks:
			if not i.text()=="":
				peakSend.append(float(i.text())) #convert user input string of peak values into float, then saved into PeakSend list
		
		return(dialog.detectorName.text(),float(dialog.maxEv.text()), peakSend, result)