"""
Short time fourier transform

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
    
def chirp(t, f0, t1, f1):
    return np.cos((f0+(f1-f0)/2*t/t1)*t)    
    
def clear_axis(ax):
    ytext = ax.get_ylabel()
    xtext = ax.get_xlabel()
    
    ax.cla()
    
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    ax.set_ylabel(ytext)
    ax.set_xlabel(xtext)
    
    ax.yaxis.set_label_coords(-0.05,0.5)
    ax.xaxis.set_label_coords(0.5,-0.05)
    
window = mexican_hat_window
#y = np.loadtxt('chirp.dat')

N = 1024

Fs = 2 * np.pi
Ts = 1 / Fs
t = np.linspace(0,N*Ts,N)

y = chirp(t,0,t[-1],0.5*2*np.pi)*np.exp(-0.02*t)

w = window(t, 10, 0)

y = np.transpose(y)
period = N / Fs

n = np.arange(1., N + 1)
frequencies = n / N * Fs

fig, ((ax, ax3), (ax2, ax4)) = plt.subplots(nrows=2, ncols=2)
plt.subplots_adjust(left=0.30, bottom=0.22, right=0.95, top=0.93, hspace=0.45)

orig, = ax.plot(t,y)
w_line, = ax.plot(t, w, 'r-')

ax.axis([0,t[-1],-max(abs(y)),max(abs(y))])
ax.spines['bottom'].set_position('zero')
ax.set_xlabel('Time (sec)')
ax.xaxis.set_label_coords(0.5,-0.05)
ax.set_title('Original Signal + Window')

windowed_y = w*y
windowed_y_line, = ax2.plot(t,windowed_y);
ax2.spines['bottom'].set_position('zero')
ax2.axis([0,t[-1],-max(abs(windowed_y)),max(abs(windowed_y))])
ax2.set_xlabel('Time (sec)')
ax2.xaxis.set_label_coords(0.5,-0.05)
ax2.set_title('Windowed Signal')

S = np.fft.fft(windowed_y)
S = np.fft.fftshift(S)[N/2:]


fft, = ax3.plot(frequencies[:N/4],abs(S[:N/4]))
ax3.axis([0, max(frequencies)/4, 0, max(abs(S))])
ax3.set_xlabel('Frequency')
ax3.set_title('FFT of Windowed Signal')

ax4.specgram(windowed_y, Fs=Fs)
ax4.axis([0, 143, 0, np.pi])
ax4.set_title("Spectrogram")

axA = plt.axes([0.30, 0.1, 0.63, 0.03], axisbg=axcolor)
axB = plt.axes([0.30, 0.06, 0.63, 0.03], axisbg=axcolor)

sliderA = Slider(axA, 'Std. Dev.', 1, max_A, valinit=10, valfmt='%i')
sliderB = Slider(axB, 'Center x', 0, max(t), valinit=0, valfmt='%i')

resetax = plt.axes([0.8, 0.020, 0.1, 0.03])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def update(val):
    a = int(sliderA.val)
    b = int(sliderB.val)
    
    w = window(t, a, b)
    w_line.set_ydata(w)
    
    windowed_y = y*w
    windowed_y_line.set_ydata(windowed_y)
    ax2.axis([0,t[-1],-max(abs(windowed_y)),max(abs(windowed_y))])
    
    S = np.fft.fft(windowed_y);
    S = np.fft.fftshift(S)[N/2:];
    
    #S_filtered = np.where(abs(S)>0.05*max(abs(S)), abs(S), 0)

    #count = np.count_nonzero(S_filtered)
    fft.set_ydata(abs(S[:N/4]))
    #print S_filtered.size, count
    #fft.set_xdata(frequencies[:count-1])
    ax3.axis([0, max(frequencies)/4, 0, max(abs(S))])
    
    clear_axis(ax4)
    ax4.specgram(windowed_y, Fs=Fs)
    ax4.axis([0, 143, 0, np.pi])
    
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