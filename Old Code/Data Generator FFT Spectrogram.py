# -*- coding: utf-8 -*-
"""
Short time fourier transform

@author: Nic P
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.widgets import Slider, Button, RadioButtons

axcolor = 'white'
exp = 0
max_freq = 5
NFFT = 80
noverlap = 40

a, b = 1, 2

def chirp(t, f0, t1, f1):
    return np.cos((f0+(f1-f0)/2*t/t1)*2*np.pi*t)

class Function:
    def __init__(self, func, range, text, title):
        self.func = func
        self.range = range
        self.text = text
        self.title = title

seq_sins = lambda a,b,t: np.where(t<t[t.size/2], np.sin(a*2*np.pi*t), np.sin(b*2*np.pi*t))
        
f1 = Function(lambda a,b,t: np.sin(a*2*np.pi*t), (0, 10), "Sinusoid", "Sinusoid")
f2 = Function(lambda a,b,t: np.sin(a*2*np.pi*t)+np.sin(b*2*np.pi*t), (0, 10), "Two Sinusoids", "Sum of Two Sinusoids")
f3 = Function(seq_sins, (0, 10), "Two Seq. Sinusoids", "Two Sequential Sinusoids")
f4 = Function(lambda a,b,t: np.where(t==t[t.size/2], 1, 0), (0, 10), "Delta", "Delta Function")
f5 = Function(lambda a,b,t: chirp(t,a,t[-1],b), (0, 10), "Chirp", "Chirp")
    
funcs = [f1, f2, f3, f4, f5]
    
def clear_axis(ax):
    ytext = ax.get_ylabel()
    xtext = ax.get_xlabel()
    
    ax.cla()
    
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    ax.set_ylabel(ytext)
    ax.set_xlabel(xtext)
    
    ax.yaxis.set_label_coords(-0.03,0.5)
    ax.xaxis.set_label_coords(0.5,-0.15)
    

N = 1024

Fs = 4 * np.pi
Ts = 1 / Fs
t = np.linspace(0,N*Ts,N)

function = f1

y = function.func(a, b, t)
if exp:
    y = y*np.exp(-0.03*t)

y = np.transpose(y)
period = N / Fs

n = np.arange(1., N + 1)
frequencies = n / N * Fs

fig, (ax, ax2, ax3) = plt.subplots(nrows=3, ncols=1)
plt.subplots_adjust(left=0.30, bottom=0.22, right=0.95, top=0.93, hspace=0.5)

orig, = ax.plot(t,y)

ax.axis([0,t[-1],-max(abs(y)),max(abs(y))])
ax.spines['bottom'].set_position('zero')
ax.set_xlabel('Time (sec)')
ax.xaxis.set_label_coords(0.5,-0.05)
ax.set_title(function.title)


S = np.fft.fft(y)
S = np.fft.fftshift(S)[N/2:]

fft, = ax2.plot(frequencies[:N/2],abs(S[:N/2]))
ax2.axis([0, 2*np.pi, 0, max(abs(S))*1.1])
ax2.xaxis.set_label_coords(0.5,-0.12)
ax2.set_xlabel('Frequency')
ax2.set_title('FFT of Signal')

spec,_,_,_ = ax3.specgram(y, Fs=Fs, NFFT=NFFT, noverlap=noverlap)
ax3.axis([0, t[-1], 0, 2*np.pi])
ax3.set_title("Spectrogram")
ax3.set_xlabel('Time (sec)')
ax3.set_ylabel('Frequency')
ax3.yaxis.set_label_coords(-0.03,0.5)
ax3.xaxis.set_label_coords(0.5,-0.15)

axA = plt.axes([0.30, 0.1, 0.63, 0.03], axisbg=axcolor)
axB = plt.axes([0.30, 0.06, 0.63, 0.03], axisbg=axcolor)

sliderA = Slider(axA, 'Freq 1', 0.1, max_freq, valinit=a, valfmt='%.2f')
sliderB = Slider(axB, 'Freq 2', 0.1, max_freq, valinit=b, valfmt='%.2f')

resetax = plt.axes([0.8, 0.020, 0.1, 0.03])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def update(val):
    a = sliderA.val
    b = sliderB.val
    
    y = function.func(a, b, t)
    if exp:
        y = y*np.exp(-0.03*t)
        
    orig.set_ydata(y)
    ax.axis([0,t[-1],-max(abs(y)),max(abs(y))])
    ax.set_title(function.title)
    
    S = np.fft.fft(y);
    S = np.fft.fftshift(S)[N/2:];

    fft.set_ydata(abs(S[:N/2]))
    ax2.axis([0, 2*np.pi, 0, max(abs(S))*1.1])
    
    clear_axis(ax3)
    ax3.specgram(y, Fs=Fs, NFFT=NFFT, noverlap=noverlap)
    ax3.axis([0, t[-1], 0, 2*np.pi])
    ax3.set_title("Spectrogram")
    
    fig.canvas.draw_idle()


def reset(event):
    sliderA.reset()
    sliderB.reset()
button.on_clicked(reset)

sliderA.on_changed(update)
sliderB.on_changed(update)


rax = plt.axes([0.025, 0.5, 0.22, 0.15], axisbg=axcolor)
rExp = plt.axes([0.025, 0.3, 0.22, 0.12], axisbg=axcolor)
radio = RadioButtons(rax, [f.text for f in funcs], active=0)
radio2 = RadioButtons(rExp, ("Exponential Decay", "none"), active=1)

for label in radio.labels + radio2.labels:
    label.set_fontsize(9.5)

def radiofunc(label):
    global function
    for f in funcs:
        if label == f.text:
            function = f
    update(0)
def radiofunc2(label):
    global exp
    if label == "none": exp = 0
    else: exp = 1
    update(0)

radio.on_clicked(radiofunc)
radio2.on_clicked(radiofunc2)
    
plt.show()