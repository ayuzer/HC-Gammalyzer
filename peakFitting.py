"""
This function is for fitting a Gaussian to a data set.
it would be very easy to add other functions using the same
pattern as the gauss_function function.
(also used for calibration)
"""

import math
import numpy as np
from scipy.optimize import curve_fit

def peakFitting(ydata,xdata=None):
    if xdata==None:
        xdata=np.arange(len(ydata))
#new code commence ,initial estimation of gaussian parameters *fix
    amp = np.max(ydata)
    mean = xdata[np.argmax(ydata)]
#/end    
    return curve_fit(gauss_function,xdata,ydata, p0=[amp,mean,0.5,0]) ##problem: attempt to get argmax of an empty sequence used to be: [1,np.argmax(ydata), 1, 0]
#p0=[a,b,c]= ampltidue, mean, sigma
def expFitting(ydata,xdata=None): #possible uses: for non linear fitting for calibration
    if xdata==None:
        xdata=np.arange(len(ydata))
    
    return curve_fit(exp_function,xdata,ydata, p0=[1,1,0,0])

def gauss_function(x,a,b,c,d): 
    return a*np.exp(-(((x-b)**2)/(2*(c**2))))+d #a = amp , b = center point, c= sigma (width factor of curve), d = vertical shift
    
def exp_function(x,a,b,c,d): 
    return a*np.exp(b*x+c)+d #a= vertical stretch, b=horizontal strectch, c= horizontal translation, d= vertical shift