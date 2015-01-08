# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:16:06 2012
Short time fourier transform

@author: Nic P
"""

from numpy import *
from pylab import *

s = loadtxt('chirp.dat')

L = len(s)
Fs = 2*pi
Ts = 1/Fs
t = linspace(0,L*Ts,L)

s=transpose(s)*10e5
period=L/Fs

N=len(t)
n=arange(1.,N+1)
frequency=n/N*Fs

fig = figure()
subplot(311)
plot(t,s)

axis([0,t[L-1],-max(abs(s)),max(abs(s))])
xlabel('Time(sec)')
title('Original Signal')

subplot(312)
plot(t,(10e5)*(1-((t-t[len(t)-1]/2)/5)**2)*exp((-((t-t[len(t)-1]/2)/5)**2)/2),'r');
xlabel('Time(sec)')
title('Window Function')

S=fft(s);
S_shift=fftshift(S);
subplot(313)
plot(frequency-Fs/2,abs(S_shift))
xlabel('Frequency(Centered)')
title('FFT of Original Signal')
subplots_adjust(hspace=.7)
show()
for b in arange(0,20,10.):
    for a in arange(1,10,5):
        figure()
        subplot(311)
        plot(t,s)
        hold(True)
        g=(10e5)*(1-((t-b)/a)**2)*exp((-((t-b)/a)**2)/2)
        plot(t,g,'r')
        axis([0,t[L-1],-max(abs(g)),max(abs(g))])
        xlabel('Time(sec)')
        title('Original signal and window function')
        hold(False)
        output=g*s
        subplot(312)
        plot(t,output)
     #   axis([0,t[L-1],-max(output),max(abs(output))])
        xlabel('Time(sec)')
        title('Windowed Signal with a='+str(a)+',b='+str(b))
        OUTPUT=fft(output)
        OUTPUT_shift=fftshift(OUTPUT)
        subplot(313)
        plot(frequency-Fs/2,abs(OUTPUT_shift))
        xlabel('Frequency (Centered)')
        title('FFT of Windowed Signal')
        subplots_adjust(hspace=.7)

        show()

figure()
k = kaiser(256,16)
specgram(s,window=k)

title('Spectrogram of Original Signal')
ss =s
show()
figure()
subplot(211)
plot(t,ss)
title('Original signal')
xlabel('Time(sec)')

SS=fft(ss);
SS_shift=fftshift(SS)
subplot(212)
plot(frequency-Fs/2,abs(SS_shift))
title('FFT of original signal')
xlabel('Frequency(Centered)')
subplots_adjust(hspace=.7)

show()

figure()
subplot(121)
specgram(ss)
title('Spectrogram of signal (hanning)')
subplot(122)
specgram(s,window=k)
title('Spectrogram of signal (kaiser)')
show()