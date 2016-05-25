"""
This Snippet acts as the starting point for the program to create an
instance of the mainwindow object and to properly exit when done 
"""

import sys
import mainWindow
from PyQt4 import QtGui

def main():
	app = QtGui.QApplication(sys.argv)
	ex=mainWindow.window() #executes mainWindow (not a variable)
	
	sys.exit(app.exec_())

if __name__=='__main__':
	main()