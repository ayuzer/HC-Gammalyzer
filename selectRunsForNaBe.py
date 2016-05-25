"""
This code creates a class that when called creates a window that
is used to input the values necessary to carrying out a 
calibration. 
"""

from PyQt4 import QtGui
from PyQt4 import QtCore

class selectRunsForNaBe(QtGui.QDialog):
	def __init__(self, backList, dataList, parent=None):
	
		super(selectRunsForNaBe, self).__init__(parent)
		
		self.formLayout=QtGui.QFormLayout()	
		self.clearButton=QtGui.QPushButton('Ok - Clear', self)		
		
		self.backList=backList
		self.dataList=dataList
		listBack=QtGui.QComboBox()
		listBack.addItems(list(self.backList))
		self.formLayout.addRow(listBack)
		
		listData=QtGui.QComboBox()
		listData.addItems(list(self.dataList))
		listData.view.setSelectionMode(len(self.dataList))
		self.formLayout.addRow(listData)
		
		self.clearButton.clicked.connect(self.accept)
		self.formLayout.addRow(self.clearButton)
		self.setLayout(self.formLayout)
		
		# self.view().pressed.connect(self.handleItemPressed)
		# self.setModel(QtGui.QStandardItemModel(self))

		# myBoxLayout = QtGui.QVBoxLayout()
		# self.setLayout(myBoxLayout)
		# self.setCentralWidget(self)
		# self.ComboBox = CheckableComboBox()
		# for i in range(3):
			# self.ComboBox.addItem("Combobox Item " + str(i))
			# item = self.ComboBox.model().item(i, 0)
			# item.setCheckState(QtCore.Qt.Unchecked)
		# self.toolbutton = QtGui.QToolButton(self)
		# self.toolbutton.setText('Select Categories ')
		# self.toolmenu = QtGui.QMenu(self)
		# for i in range(3):
			# action = self.toolmenu.addAction("Category " + str(i))
			# action.setCheckable(True)
		# self.toolbutton.setMenu(self.toolmenu)
		# self.toolbutton.setPopupMode(QtGui.QToolButton.InstantPopup)
		# myBoxLayout.addWidget(self.toolbutton)
		# myBoxLayout.addWidget(self.ComboBox)
		   
	# def handleItemPressed(self, index):
		# item = self.model().itemFromIndex(index)
		# if item.checkState() == QtCore.Qt.Checked:
			# item.setCheckState(QtCore.Qt.Unchecked)
		# else:
			# item.setCheckState(QtCore.Qt.Checked)