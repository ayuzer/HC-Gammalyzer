"""
The Following Code is for the creation of an exe file from the python code.
Essentially a makefile
"""

import sys
import scipy
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages":["os",'scipy',
					'scipy.optimize'],
					'namespace_packages':['PyQt4','matplotlib','pickle','math'],
					"includes": ['binaryRead','detectorRun','mainWindow','chanCheck',
					'parse','binaryRead','breakUp','plotting', 'getInfWin',
					'calibration','impExp','simpleBreak','peakFitting',
					'mpldatacursor','printWin','numpy',],
					"compressed":(1),
					"include_files":['web.png','open_folder.png','exit.png','10x10.png'],
					"excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).

base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(  name = "Gammalyzer",
        version = "1.0",
        description = "Gammalyzer Application",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base,icon='web.ico')])