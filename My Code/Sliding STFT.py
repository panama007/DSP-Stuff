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
import matplotlib.pyplot as plt							                    # contains plotting functions
import Tkinter as Tk
from matplotlib.widgets import Slider, Button, RadioButtons	# contains sliders/buttons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


#####################################
##  Definitions for Windows and Signal
##     and other functions
##
#####################################

filenames = os.listdir("signals/")                                             # different signals
axcolor = 'white'
max_A = 50										                                    # max standard deviation
global y

def choose_signal(i):
    global y
    y = np.loadtxt('signals/'+filenames[i])
    y /= max(max(y),-min(y))

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


window = mexican_hat_window                                             # initially the window is set to mexican hat
choose_signal(2)

N = len(y)                                                                             # number of data points to use

Fs = 2 * np.pi
Ts = 1 / Fs
t = np.linspace(0,N*Ts,N)

w = window(t, 10, 0)

period = N / Fs

n = np.arange(1., N + 1)                                                       # list of indeces. n = [1,2,3....1024]
frequencies = n / N * Fs                                                         # frequencies = [1/1024*2pi, 2/1024*2pi, ....1024/1024*2pi]

fig = matplotlib.figure.Figure()
ax = fig.add_subplot(221)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(222)
ax4 = fig.add_subplot(224)
fig.subplots_adjust(left=0.30, bottom=0.22, right=0.95, top=0.93, hspace=0.45)  # sets the spacing limits on the 4 plots

canvas = FigureCanvasTkAgg(fig,master=root)#no resize callback as of now
canvas.get_tk_widget().pack(side=Tk.BOTTOM)



#####################################
##  Creates all the plots
##
#####################################

orig, = ax.plot(t,y)                                                                # plots the signal
w_line, = ax.plot(t, w, 'r-')                                                     # plots the window on the same graph

ax.axis([0,t[-1],-max(abs(y)),max(abs(y))])                             # adjusts the graph range, the x and y ranges
ax.spines['bottom'].set_position('zero')                                  #     adjusts the labels, title
ax.set_xlabel('Time (sec)')
ax.xaxis.set_label_coords(0.5,-0.05)
ax.set_title('Original Signal + Window')

windowed_y = w*y                                                                # calculates the windowed signal = window*signal
windowed_y_line, = ax2.plot(t,windowed_y);                          #   plots it
ax2.spines['bottom'].set_position('zero')
ax2.axis([0,t[-1],-max(abs(windowed_y)),max(abs(windowed_y))])   # adjusts the graphing range and labels
ax2.set_xlabel('Time (sec)')
ax2.xaxis.set_label_coords(0.5,-0.05)
ax2.set_title('Windowed Signal')

S = np.fft.fft(windowed_y)                                                     # calculates the FFT of the windowed signal
S = np.fft.fftshift(S)[N/2:]                                                      # shift so that zero frequency is at the start instead of middle

fft, = ax3.plot(frequencies[:N/2],abs(S[:N/2]))                        # plots the FFT of windowed signal
ax3.axis([0, max(frequencies)/4, 0, max(abs(S))])                  # adjusts the plotting range
ax3.set_xlabel('Frequency')
ax3.set_title('FFT of Windowed Signal')

ax4.specgram(windowed_y, Fs=Fs)                                       # plots the spectrogram of the signal
ax4.axis([0, (len(y)-128)*Ts, 0, np.pi])
ax4.set_title("Spectrogram")

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


def update(val):                                                                            # function to be run whenever a slider changes value
    N = len(y)                                                                                 # number of data points to use
    Fs = 2 * np.pi
    Ts = 1 / Fs
    t = np.linspace(0,N*Ts,N)
    period = N / Fs
    n = np.arange(1., N + 1)                                                           # list of indeces. n = [1,2,3....1024]
    frequencies = n / N * Fs                                                            #   frequencies = [1/1024*2pi, 2/1024*2pi, ....1024/1024*2pi]

    a = int(sliderA.val)                                                                    #   retrieve the std. dev. from the slider
    b = int(sliderB.val)                                                                    #   retrieve the center/mean from the slider

    clear_axis(ax)
    clear_axis(ax2)  
    clear_axis(ax3)  
    clear_axis(ax4)
  
    ax.plot(t, y)
    
    w = window(t, a, b)                                                                   # recalculate the window
    ax.plot(t,w, 'r-')
    ax.axis([0, t[-1], -max(abs(y)),max(abs(y))])

    windowed_y = y*w                                                                    # recalculates the windowed signal
    
    ax2.plot(t, windowed_y)    
    ax2.axis([0,t[-1],-max(abs(windowed_y)),max(abs(windowed_y))])  
    
    S = np.fft.fft(windowed_y);                                                         # recalculate the FFT of the windowed signal
    S = np.fft.fftshift(S)[N/2:];

    ax3.plot(frequencies[:N/2], (abs(S[:N/2])))                                                         # replots the FFT
    ax3.axis([0, max(frequencies)/4, 0, max(abs(S))])
    
    ax4.specgram(windowed_y, Fs=Fs)
    ax4.axis([0, (N-128)*Ts, 0, np.pi])

    fig.canvas.draw_idle()                                         # must be executed to update the display

sliderA.on_changed(update)                                                          # attaches the "update" function to both sliders
sliderB.on_changed(update)

def reset(event):                                                                           # the function to be run when the reset button is pressed
    sliderA.reset()
    sliderB.reset()

button.on_clicked(reset)                                                                # attaches the "reset" function to the button


rax = fig.add_axes([0.025, 0.5, 0.22, 0.15], axisbg=axcolor)                  # creates the box for selecting a window
rax.set_title("Windows")
radio = RadioButtons(rax, ("Mexican Hat", "Gabor", "none"), active=0)

for label in radio.labels:                                                              # adjusts the font size of the window names
    label.set_fontsize(9.2)

def radiofunc(label):                                                                     # function to be run when a different window is selected
    global window
    if label == "Mexican Hat":
        window = mexican_hat_window
    elif label == "Gabor":
        window = gabor_window
    else:
        window = lambda t,a,b: np.ones(t.size)                               # window = [1,1,....1]
    update(0)                                                                                # updates the plots since we changed the window

radio.on_clicked(radiofunc)                                                            # attaches the "radiofunc" to our radio buttons.
    
    
#Create a toplevel menu (for selecting matrices)
menubar = Tk.Menu(root)

#Create the Matrix pulldown menu, and add it to the menubar
filemenu = Tk.Menu(menubar,tearoff=0)
for i, name in enumerate(filenames):
    expression = \
    'filemenu.add_command(label=name,command=lambda : update(choose_signal({})))'.format(i)
    eval(expression)
menubar.add_cascade(label="Signal From File",menu=filemenu)


#Display the menu
root.config(menu=menubar)

#Draw the plot on the canvas
canvas.show()

Tk.mainloop()


#plt.show()                                                      # must be run in order to see the plots
