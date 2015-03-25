import numpy as np
from numpy import pi
import pywt
from scipy import signal

def mexh(points, a):
    x = np.linspace(-points/2.+.5, points/2.-.5, points)
    xsq = x**2
    asq = a**2
    A = 2/(3*a)**.5/pi**.25
    return signal.ricker(points, a)
    return A*(1-xsq/asq)*np.exp(-xsq/2/asq)
    
def morl(points, a):
    return 1/a**.5*signal.morlet(points, s=a)
    
def other(points, a, name):
    if a <= 1: a = 1
    w = pywt.Wavelet(name)
    f = w.wavefun(15)[1]
    N = len(f)
    x = np.linspace(N/2*(1-1./a), N-N/2*(1-1./a)-1, points)
    #print N, x
    return [1/a**.5*f[i] for i in x]
    
#def shan(points, a):
    
    
    
