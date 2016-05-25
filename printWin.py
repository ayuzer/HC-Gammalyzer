"""
The following provides an alternative implementation for stdout and stderr, (python interpreter console outputs)
this is for the purpose of having print statements and error messages be
delivered to the user in a popup box.
"""

import gc
import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

class printWin(QtGui.QDialog):
    def __init__(self, parent=None):
        super(printWin, self).__init__(parent)    
        self.formLayout=QtGui.QFormLayout()    
        self.clearButton=QtGui.QPushButton('Ok - Clear', self)
        self.edit = QtGui.QTextEdit(self)    
        self.edit.setReadOnly(True)
        self.formLayout.addRow(self.edit)
        self.clearButton.clicked.connect(self.clearAll)
        self.clearButton.clicked.connect(self.accept)
        self.formLayout.addRow(self.clearButton)
        self.setLayout(self.formLayout)

    def write(self, text):    
        self.edit.insertPlainText(text)
        QtGui.QApplication.processEvents
        self.show()
        
        
  

    def clearAll(self):
        self.edit.deleteLater()
        gc.collect()
        self.edit = QtGui.QTextEdit(self)    
        self.edit.setReadOnly(True)
        self.formLayout.insertRow(0,self.edit)
        self.setLayout(self.formLayout)
        
    def flush(self):
        pass