"""
This module is a set of functions to save and reload the calibration or
detectorRun objects. this makes analysis times much easier and shorter
when revisiting data that has already been analyzed once.
"""

import pickle

def saveToFile(object,name):
	with open(name, "wb") as f:
		pickle.dump(object,f)
	
def loadFromFile(file):
	reObj=[]
	for i in file:
		with open(i,"rb") as f:
			reObj.append(pickle.load(f))
	
	return reObj