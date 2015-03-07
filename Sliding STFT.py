"""
Short Time Fourier Transform with adjustable sliding window

By: Alex Barreiro

"""


#####################################
##  Packages to import
##     contains something necessary but isn't default part of python
##
#####################################

import numpy as np									                            # contains numerical computation functions
import matplotlib
matplotlib.use('TkAgg')
from mpl_toolkits.mplot3d.axes3d import Axes3D
#import matplotlib.pyplot as plt							                    # contains plotting functions
import Tkinter as Tk
from matplotlib import cm
from matplotlib.widgets import Slider, Button, RadioButtons	# contains sliders/buttons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.pyplot import setp
from matplotlib.figure import Figure
import time

import os


#####################################
##  Definitions for Windows and Signal
##     and other functions
##
#####################################

filenames = os.listdir("signals2/")                                             # different signals
axcolor = 'white'
max_A = 50										                                    # max standard deviation
global y
spec_plot = 0
lines = []
signalname = ''

def local_maxima(xval, yval):
    xval = np.asarray(xval)
    yval = np.asarray(yval)

    sort_idx = np.argsort(xval)
    yval = yval[sort_idx]
    gradient = np.diff(yval)
    maxima = np.diff((gradient > 0).view(np.int8))
    maxima = np.concatenate((([0],) if gradient[0] < 0 else ()) +
                          (np.where(maxima == -1)[0] + 1,) +
                          (([len(yval)-1],) if gradient[-1] > 0 else ()))
                          
                          
    os.system('cls' if os.name == 'nt' else 'clear')
    print "\nFrequency\tAmplitude\n-----------------------"
    indeces = np.argsort(map(lambda x: -yval[x], maxima))
    for m in maxima[indeces][:10]:
        print "%f\t%f" % (xval[m], yval[m])

def transform_complex(line):
    return line.replace(b'+-', b'-')

def choose_signal(i):
    global y, signalname
    with open('signals2/'+filenames[i], 'rb') as f:
        lines = map(transform_complex, f)
        y = np.loadtxt(lines, dtype=np.complex128)
    y /= max(abs(y))
    signalname = filenames[i][:-4]

def mexican_hat_window(t, a, b):						                    # mexican hat window. b = midpoint/mean, a = std. dev
    return (1-((t-b)/a)**2)*np.exp((-((t-b)/a)**2)/2)

def gabor_window(t, a, b):							                            # gabor window. b = midpoint, a = std. dev
    return np.exp((-((t-b)/a)**2)/2)
    
def chirp(t, f0, t1, f1):								                            # chirp. sinusoid whose frequency varies 
    return np.cos((f0+(f1-f0)/2*t/t1)*t)    					            #   linearly from f0 to f1 over the time 0-t1
    
def clear_axis(ax):									                                # function to clear a graph but keep the labels/title
    ytext = ax.get_ylabel()
    xtext = ax.get_xlabel()
    title   = ax.get_title()

    ax.cla()
    
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    ax.set_ylabel(ytext)
    ax.set_xlabel(xtext)
    ax.set_title(title)
    
    ax.yaxis.set_label_coords(-0.05,0.5)                                 # aligns the labels so it looks good
    ax.xaxis.set_label_coords(0.5,-0.1)
    
#####################################
##  Initialization and definition of some variables
##
#####################################

root = Tk.Tk()
root.wm_title('Sliding STFT')

windows = {"Mexican Hat": mexican_hat_window , "Gabor" : gabor_window, "none" : lambda t,a,b: np.ones(t.size)}
window = windows["Mexican Hat"]                                          # initially the window is set to mexican hat
choose_signal(2)


N = len(y)                                                                             # number of data points to use

Fs = 2 * np.pi
Ts = 1 / Fs
t = np.linspace(0,N*Ts,N)

w = window(t, 10, 0)

period = N / Fs

n = np.arange(1., N + 1)                                                       # list of indeces. n = [1,2,3....1024]
frequencies = n / N * Fs                                                         # frequencies = [1/1024*2pi, 2/1024*2pi, ....1024/1024*2pi]

fig = Figure()
ax = fig.add_subplot(221)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(222)
ax4 = fig.add_subplot(224)
fig.subplots_adjust(left=0.30, bottom=0.22, right=0.95, top=0.93, hspace=0.45)  # sets the spacing limits on the 4 plots

canvas = FigureCanvasTkAgg(fig,master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)



#####################################
##  Creates all the plots
##
#####################################

orig, = ax.plot(t,y)                                                                # plots the signal
w_line, = ax.plot(t, w, 'r-')                                                     # plots the window on the same graph
lines.append([orig, w_line])

ax.axis([0,t[-1],-max(abs(y)),max(abs(y))])                             # adjusts the graph range, the x and y ranges
ax.spines['bottom'].set_position('zero')                                  #     adjusts the labels, title
ax.set_xlabel('Time (sec)')
ax.xaxis.set_label_coords(0.5,-0.05)
ax.set_title(signalname)

windowed_y = w*y                                                                # calculates the windowed signal = window*signal
windowed_y_line, = ax2.plot(t,windowed_y);                          #   plots it
lines.append(windowed_y_line)
ax2.spines['bottom'].set_position('zero')
ax2.axis([0,t[-1],-max(abs(windowed_y)),max(abs(windowed_y))])   # adjusts the graphing range and labels
ax2.set_xlabel('Time (sec)')
ax2.xaxis.set_label_coords(0.5,-0.05)
ax2.set_title('Windowed Signal')

S = np.fft.fft(windowed_y)                                                     # calculates the FFT of the windowed signal
S = np.fft.fftshift(S)[N/2:]                                                      # shift so that zero frequency is at the start instead of middle

fft, = ax3.plot(frequencies[:N/2],abs(S[:N/2]))                        # plots the FFT of windowed signal
lines.append(fft)
ax3.axis([0, max(frequencies)/2, 0, max(abs(S))])                  # adjusts the plotting range
ax3.set_xlabel('Frequency')
ax3.set_title('FFT of Windowed Signal')

ax4.specgram(windowed_y, Fs=Fs)                                       # plots the spectrogram of the signal
ax4.axis([0, (len(y)-128)*Ts, 0, np.pi])
ax4.set_title("Spectrogram")
ax4.set_xlabel('Time (sec)')
ax4.set_ylabel('Frequency')

#####################################
##    Sliders, Button, and Choice Boxes
##
#####################################

axA = fig.add_axes([0.30, 0.1, 0.63, 0.03], axisbg=axcolor)         # creates the sliders for adjusting the window
axB = fig.add_axes([0.30, 0.06, 0.63, 0.03], axisbg=axcolor)

sliderA = Slider(axA, 'Std. Dev.', 1, max_A, valinit=10, valfmt='%i')   # adds label, sets initial value, sets range for sliders
sliderB = Slider(axB, 'Center x', 0, max(t), valinit=0, valfmt='%i')

resetax = fig.add_axes([0.8, 0.020, 0.1, 0.03])                                 # reset button, which will reset the sliders
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def update(_):                                                                            # function to be run whenever a slider changes value
    test = time.time()
    N = len(y)                                                                                 # number of data points to use
    Fs = 2 * np.pi
    Ts = 1 / Fs
    t = np.linspace(0,N*Ts,N)
    '''
    period = N / Fs
    n = np.arange(1., N + 1)                                                           # list of indeces. n = [1,2,3....1024]
    frequencies = n / N * Fs                                                            #   frequencies = [1/1024*2pi, 2/1024*2pi, ....1024/1024*2pi]
    '''
    frequencies = np.fft.fftfreq(N, d=Ts)[:N/2]
    
    a = int(sliderA.val)                                                                    #   retrieve the std. dev. from the slider
    sliderB.valmax = t[-1]
    b = int(sliderB.val)                                                                    #   retrieve the center/mean from the slider

    #clear_axis(ax4)
    
    w = window(t, a, b)                                                                   # recalculate the window
    ax.axis([0, t[-1], -max(abs(y)),max(abs(y))])
    ax.set_title(signalname)

    windowed_y = y*w                                                                    # recalculates the windowed signal
    ax2.axis([0,t[-1],-max(abs(windowed_y)),max(abs(windowed_y))]) 
         
    
    S = abs(np.fft.fft(windowed_y)[:N/2])                                                        # recalculate the FFT of the windowed signal
    #S = np.fft.fftshift(S)#[N/2:]
    ax3.axis([0, max(frequencies), 0, max(S)])
    
    setp(lines[0][0], xdata=t, ydata=y)
    setp(lines[0][1], xdata=t, ydata=w)
    setp(lines[1], xdata=t, ydata=windowed_y)
    setp(lines[2], xdata=frequencies, ydata=S)
    
    local_maxima(frequencies, S)
    
    if spec_plot == 0:
        ax4 = fig.add_subplot(224)
        ax4.specgram(windowed_y, Fs=Fs)
        ax4.axis([0, (N-128)*Ts, 0, np.pi])
        ax4.set_title('Spectrogram')
    
    elif spec_plot == 1:
        ax4 = fig.add_subplot(224, projection='3d')
        z = []
        for i in range(0,N-128):
            xdata = t[i:i+256]
            ydata = windowed_y[i:i+256]
            zdata = np.fft.fftshift(np.fft.fft(ydata, n=N))[N/2:]
            z.append(np.log(abs(zdata)))
        l = len(t[:-128])
        ax4.plot_surface([[t[j]]*(N/2) for j in range(l)], [frequencies[:N/2]]*l, z, rstride=32, cstride=32, cmap=cm.jet, linewidth=0)
        ax4.set_title('3D Spectrogram')
        
    ax4.set_xlabel('Time (sec)')
    ax4.set_ylabel('Frequency')
    
    #print time.time()-test
    fig.canvas.draw()                                         # must be executed to update the display

sliderA.on_changed(update)                                                          # attaches the "update" function to both sliders
sliderB.on_changed(update)

def reset(event):                                                                           # the function to be run when the reset button is pressed
    sliderA.reset()
    sliderB.reset()

button.on_clicked(reset)                                                                # attaches the "reset" function to the button


rax = fig.add_axes([0.025, 0.7, 0.22, 0.15], axisbg=axcolor)                  # creates the box for selecting a window
rax.set_title("Windows")
radio = RadioButtons(rax, ("Mexican Hat", "Gabor", "none"), active=0)

rax2 = fig.add_axes([0.025, 0.45, 0.22, 0.15], axisbg=axcolor)
rax2.set_title("Spectrogram Plot")
radio2 = RadioButtons(rax2, ("2d Color Plot", "3d Plot"), active=0)

for label in radio.labels + radio2.labels:                                                              # adjusts the font size of the window names
    label.set_fontsize(9.2)

def radiofunc(label):                                                                     # function to be run when a different window is selected
    global window
    window = windows[label]                                                            # window = [1,1,....1]
    update(0)                                                                                # updates the plots since we changed the window

def radiofunc2(label):
    global spec_plot
    spec_plot = 1 if label == "3d Plot" else 0 
    update(0)
    
radio.on_clicked(radiofunc)                                                            # attaches the "radiofunc" to our radio buttons.
radio2.on_clicked(radiofunc2)    
    
#Create a toplevel toolbar
menubar = Tk.Menu(root)

#Create the file selector in the toolbar
filemenu = Tk.Menu(menubar,tearoff=0)
for i, name in enumerate(filenames):
    expression = \
    'filemenu.add_command(label=name[:-4],command=lambda : update(choose_signal({})))'.format(i)
    eval(expression)
menubar.add_cascade(label="Signal From File",menu=filemenu)


#Display the menu
root.config(menu=menubar)

Tk.mainloop()

