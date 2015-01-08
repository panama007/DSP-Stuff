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
max_A = 50

def mexican_hat_window(t, a, b):
    return (1-((t-b)/a)**2)*np.exp((-((t-b)/a)**2)/2)

def gabor_window(t, a, b):
    return np.exp((-((t-b)/a)**2)/2)
    
window = mexican_hat_window
y = np.loadtxt('chirp.dat')

N = len(y)
Fs = 2 * np.pi
Ts = 1 / Fs
t = np.linspace(0,N*Ts,N)

w = window(t, 1, 0)

y = np.transpose(y)
period = N / Fs

n = np.arange(1., N + 1)
frequencies = n / N * Fs

fig, (ax, ax2, ax3) = plt.subplots(nrows=3, ncols=1)
plt.subplots_adjust(left=0.30, bottom=0.22, right=0.95, top=0.93, hspace=0.50)

orig, = ax.plot(t,y)
w_line, = ax.plot(t, w, 'r-')

ax.axis([0,t[-1],-max(abs(y)),max(abs(y))])
ax.spines['bottom'].set_position('zero')
ax.set_xlabel('Time (sec)')
ax.xaxis.set_label_coords(0.5,-0.05)
ax.set_title('Original Signal')

windowed_y = w*y
windowed_y_line, = ax2.plot(t,windowed_y);
ax2.spines['bottom'].set_position('zero')
ax2.axis([0,t[-1],-max(abs(windowed_y)),max(abs(windowed_y))])
ax2.set_xlabel('Time (sec)')
ax2.xaxis.set_label_coords(0.5,-0.05)
ax2.set_title('Window Function')

S = np.fft.fft(windowed_y);
S_shift = np.fft.fftshift(S);


fft, = ax3.plot(frequencies-Fs/2,abs(S_shift))
ax3.axis([0, max(frequencies)/2, 0, max(abs(S_shift))])
ax3.set_xlabel('Frequency (Centered)')
ax3.set_title('FFT of Windowed Signal')

axA = plt.axes([0.30, 0.1, 0.63, 0.03], axisbg=axcolor)
axB = plt.axes([0.30, 0.06, 0.63, 0.03], axisbg=axcolor)

sliderA = Slider(axA, 'Std. Dev.', 1, max_A, valinit=1, valfmt='%i')
sliderB = Slider(axB, 'Center x', 0, max(t), valinit=0, valfmt='%i')

resetax = plt.axes([0.8, 0.020, 0.1, 0.03])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def update(val):
    a = int(sliderA.val)
    b = int(sliderB.val)
    
    if a == 5: sliderA.label = "FIVE"
    else: sliderA.label = "penis"
    
    w = window(t, a, b)
    w_line.set_ydata(w)
    
    windowed_y = y*w
    windowed_y_line.set_ydata(windowed_y)
    ax2.axis([0,t[-1],-max(abs(windowed_y)),max(abs(windowed_y))])
    
    S = np.fft.fft(windowed_y);
    S_shift = np.fft.fftshift(S);
    ax3.axis([0, max(frequencies)/2, 0, max(abs(S_shift))])

    fft.set_ydata(abs(S_shift))
    
    fig.canvas.draw_idle()


def reset(event):
    sliderA.reset()
    sliderB.reset()
button.on_clicked(reset)

sliderA.on_changed(update)
sliderB.on_changed(update)


rax = plt.axes([0.025, 0.5, 0.22, 0.15], axisbg=axcolor)
radio = RadioButtons(rax, ("Mexican Hat Window", "Gabor Window", "none"), active=0)

for label in radio.labels:
    label.set_fontsize(9.2)

def radiofunc(label):
    global window
    if label == "Mexican Hat Window":
        window = mexican_hat_window
    elif label == "Gabor Window":
        window = gabor_window
    else:
        window = lambda t,a,b: np.ones(t.size)
    update(0)

radio.on_clicked(radiofunc)
    
plt.show()