"""
Data generator.

This program generates data representing various scenarios, one scenario at the time.

"""

import numpy                                    # import everything numericar from library: numpy
from pylab import *                             # import plotting utilities from library: pylab
#from scipy.signal import *                      # import frequently used signals
import matplotlib.pyplot as plt

def chirp(t, f0, t1, f1):
    return np.cos((f0+(f1-f0)/2*t/t1)*t)


def write_matlab(filename, t, y):
    "Helper function that writes two arrays to matlab format"
    f = open(filename, 'w')
    for i in arange(0, len(t)):
        f.write(str(t[i]).strip("()")+'\t'+str(y[i]).strip("()")+'\n')
    f.close()


Na = 2**8
(t,ts) = linspace(0.,8*pi,Na,retstep=True)      # creates a domain [0,8pi] with 2^10 elements
ff = linspace(0, 2*pi, Na )


totaltime = t[-1]-t[0]
print "Sampling period:", ts, "(ms)"

                       
                       

(a,b)=(1,2) 
y0 = (2*sin(2*np.pi*a*t), 'One sinusoidal')
y1 = (2*(sin(2*np.pi*a*t)+sin(2*np.pi*b*t)), 'Superposition of two sinusoidals') 
y2 = (4*(sin(2*np.pi*a*t)*(t<4*pi) + sin(2*np.pi*b*t)*(t>=4*pi)), 'Two sequential sinusoidals')    # we get sin(t) for [0,4pi] and sin(2t) for [4pi,8pi]      
y3 = (2*(sin(2*np.pi*a*t)+sin(2*np.pi*b*t))*exp(-.1*t), 'Superposition of two sinusoidals with exponential decay')          
y4 = ((4*(sin(2*np.pi*a*t)*(t<4*pi) + sin(2*np.pi*b*t)*(t>=4*pi)))*exp(-.1*t), 'Sequential sinusoidals with exponential decay')
y5 = (chirp(t,0,4*pi,2*pi)*exp(-.2*t), 'Chirp')

(gamma1, w1_0) = (.2, 3)
y6 = (1*exp(-gamma1*t)*exp(1j*w1_0*t), 'Free Induction Decay')
y7 = (1*exp(-gamma1*t)*exp(1j*w1_0*t**2), 'Free Induction Decay')

(gamma2, w2_0) = (1.5, 20)
y8 = (1*exp(-gamma1*t)*exp(1j*w1_0*t) + 1*exp(-gamma2*t)*exp(1j*w2_0*t), 'Free Induction Decay')
y9 = (1*exp(-gamma1*t)*exp(1j*w1_0*t**2) +  1*exp(-gamma2*t)*exp(1j*w2_0*t**2), 'Free Induction Decay')

y = y5
function = y[0]
function_title = y[1]


numpy.savetxt(function_title+'.dat',function)
#figure(i)
f, axarr = plt.subplots(2)
y = function
F = numpy.fft.fft(y)
f = numpy.fft.fftfreq(y.size, d=ts)

#subplot(2,1,1)

axarr[0].set_title(function_title)
axarr[0].plot(t,real(y))
axarr[1].plot(f[:f.size/2],np.abs(F)[:F.size/2])
#xlabel('time (ms)')                    
#ylabel('amplitude (mV)')
    

show()
