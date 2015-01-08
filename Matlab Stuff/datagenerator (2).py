# -*- coding: utf-8 -*-
"""
Data generator.

This program generates data representing various scenarios for comparison 
between fourier and wavelet analysis. 

"""

from numpy import * # import everything numerical from library: numpy
from pylab import * # import plotting utilities from library: pylab
#from scipy.signal import * # import frequently used signals

def chirp(t, f0, t1, f1):
    return cos((f0+(f1-f0)/2*t/t1)*t)

def write_matlab(filename, t, y):
    "Helper function that writes two arrays to matlab format"
    f = open(filename, 'w')
    for i in arange(0, len(t)):
        f.write(str(t[i]).strip("()")+'\t'+str(y[i]).strip("()")+'\n')
    f.close()



Na = 2**10
(t,ts) = linspace(0.,8*pi,Na,retstep=True) # creates a domain [0,8pi] with 2^10 elements
ff = linspace(0, 2*pi, Na )
fs = 1./ts

totaltime = 8*pi
print "Sampling period:", ts, "(ms)"
print "Sampling frequency:", fs, "(KHz)" 
                       
                       
(a,b)=(10,20) 

y0 = 2*sin(a*t)                      
y1 = 2*(sin(a*t)+sin(b*t))
y2 = 4*(sin(a*t)*(t<4*pi) + sin(b*t)*(t>=4*pi)) # we get sin(t) for [0,4pi] and
                                                    # sin(2t) for [4pi,8pi]
                                                    
                                                    
y3 = y1*exp(-.1*t)
y4 = y2*exp(-.1*t)

y5 = zeros(size(t))
y5[len(y5)/2]=1

#(f_0, beta, delta) = (20, 5, 7.1)
#f_0 = 5
#beta = 4
#delta = 7.1
#am = t*(t<pi)/max(t*(t<pi))+(t>=pi)*(t<6*pi)+exp(-2*t)*(t>=6*pi)
#y6 = cos(2*pi*(f_0*t+1/2*beta*t**2+1/6*delta*t**3))*am


y6 = chirp(t,0,4*pi,1*pi)*exp(-.2*t)

(gamma, w_0) = (.2, 3)

y7 = exp(-gamma*t)*exp(1j*w_0*t)
y8 = exp(-gamma*t)*exp(1j*w_0*t**2)
y9 = exp(-gamma*t)*exp(1j*w_0*-t)
y10 = exp(-gamma*t)*exp(1j*w_0*-t**2)

(gamma2, w2_0) = (1.5, 20)

y11 = y7 +  exp(-gamma2*t)*exp(1j*w2_0*t)
y12 = y8 +  exp(-gamma2*t)*exp(1j*w2_0*t**2)
y13 = y9 +  exp(-gamma2*t)*exp(1j*w2_0*-t)
y14 = y10 + exp(-gamma2*t)*exp(1j*w2_0*-t**2)
y15 = y1 +40*y5
functions = [y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15]
functions_title = [ 'One sinusoidal', 'Superposition of two sinusoidals', \
                    'Two sequential sinusoidals',\
                    'Superposition of two sinusoidals with exponential decay',\
                    'Sequential sinusoidals with exponential decay',\
                    'Delta function',\
                    'chirp', '$e^{-' + str(gamma) +'t}e^{j'+str(w_0)+'t}$',\
                    '$e^{-' + str(gamma) +'t}e^{j'+str(w_0)+'t^2}$',\
                    '$e^{-' + str(gamma) +'t}e^{-j'+str(w_0)+'t}$',\
                    '$e^{-' + str(gamma) +'t}e^{-j'+str(w_0)+'t^2}$',\
                    '$e^{-' + str(gamma) +'t}e^{j'+str(w_0)+'t}$+' + \
                    '$e^{-' + str(gamma2) +'t}e^{j'+str(w2_0)+'t}$',\
                    '$e^{-' + str(gamma) +'t}e^{j'+str(w_0)+'t^2}$+' +\
                    '$e^{-' + str(gamma2) +'t}e^{j'+str(w2_0)+'t^2}$',\
                    '$e^{-' + str(gamma) +'t}e^{-j'+str(w_0)+'t}$+' +\
                    '$e^{-' + str(gamma2) +'t}e^{-j'+str(w2_0)+'t}=$',\
                    '$e^{-' + str(gamma) +'t}e^{-j'+str(w_0)+'t^2}+$' +\
                    '$e^{-' + str(gamma2) +'t}e^{-j'+str(w2_0)+'t^2}$', \
                    'Two sinusoidal with superposition and a delta function']

for i in range(0,len(functions)):
    #write_matlab((functions_title[i]+'.dat'),t,functions[i])
    savetxt(functions_title[i]+'.dat',functions[i])
    figure(i)
    y = functions[i]
    
    subplot(3,1,1)
    
    title(functions_title[i])
    plot(t,real(y))
    xlabel('time (ms)')                    
    ylabel('amplitude (mV)')
    
#    subplot(312)    
#    plot(t,unwrap(angle(y)))
#
#    title('phase')
#    xlabel('time (ms)')
#    ylabel('phase (rads)')

    subplot(312)
    title('Fourier transform')
    plot(t,abs(fft(y)/(2*pi))*ts)
    xlabel('frequency (2*pi rad/s)')
    ylabel('amplitude (mV)')

   
    subplot(313)
    specgram(y)
    xlabel('time (ms)')
    ylabel('frequency (2*pi rad/s)')

                    

show()
