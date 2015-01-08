import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
from helper_functions import *
import os

filenames = os.listdir("signals/")                                             # different signals
filename = 'G31722.dat'
levels = range(-1,8)
N = 8
mode = "reconstruction"
    
fig, (ax,ax2) = plt.subplots(nrows=2, ncols=1)
plt.subplots_adjust(left=0.30, bottom=0.1, right=0.95, top=0.93)


#def draw():
f = np.loadtxt('signals/'+filename)
#f = f[:256]

M = len(f)
n = int(log(M)/log(2)+0.5)
MM = 2**n
if (M > MM):
    f = f[0:MM]
elif (M < MM):
    f = f + [0]*(MM-M)
M = MM

(A, a) = mra(f, N)

(nRow, nCol) = (len(A), len(A[0])) 
NN = int(nCol/2. + 0.5)
delta_w = 2*pi/(nCol-1)
w = np.linspace(0, delta_w*(NN-1), num=NN)
t = np.arange(M)

FF = fft(f)
FF = np.abs(FF[:NN])

l, = ax.plot(t,f, lw=2, color='red')
l2, = ax2.plot(w, FF, lw=2, color='red')

ax.axis([0, M, min(f), max(f)])
ax2.axis([min(w), max(w), min(FF), max(FF)])

ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')
ax2.spines['bottom'].set_position('zero')
ax2.spines['left'].set_position('zero')

ax.set_title("Original Signal", fontsize=12)
ax2.set_title("Fourier Transform", fontsize=12)

ax.set_ylabel("Amplitude", fontsize=10)
ax2.set_ylabel("Amplitude", fontsize=10)

ax.yaxis.set_label_coords(-0.05,0.5)
ax2.yaxis.set_label_coords(-0.05,0.5)

axcolor = 'white'

def title(levels):
    if len(levels) == 9:
        return "Original Signal"
    elif len(levels) == 1:
        return "Level %i" % levels[-1]
    else:
        string = 'Levels '
        for i, level in enumerate(levels):
            string += str(level) + " +"
        return string[:-2]

def update():
    f = np.loadtxt('signals/'+filename)
   #f = f[:256]
    (A, a) = mra(f, N)
    A[0] = [sum(A[0])/len(A[0])]*len(A[0])
    
    s = np.zeros(len(f))
    for i in levels:
        s += A[i+1]
        
    FF = np.abs(fft(s)[:NN])   
    l.set_ydata(s)
    ax.set_title(title(levels))
    l2.set_ydata(FF)
    
    ax.axis([0, M, min(s), max(s)])
    ax2.axis([min(w), max(w), min(FF), max(FF)])
    
    fig.canvas.draw_idle()


#rc('text', usetex=True)
rax = plt.axes([0.025, 0.7, 0.15, 0.10], axisbg=axcolor)
rax.set_title("Select Signal")
rMode = plt.axes([0.025, 0.5, 0.15, 0.10], axisbg=axcolor)
rMode.set_title("Mode")
rCheck = plt.axes([0.025, 0.2, 0.15, 0.2], axisbg=axcolor)
rCheck.set_title("Select Level")


radio = RadioButtons(rax, filenames, active=1)
modes = RadioButtons(rMode, ["Decomposition", "Reconstruction"], active =1)
check = RadioButtons(rCheck, ["Level "+str(i) for i in range(-1,8)], active=8)
#check = CheckButtons(rCheck, ["Level "+str(i) for i in range(-1,8)], (True,True,True,True,True,True,True,True, True))

for label in radio.labels + check.labels + modes.labels:
    label.set_fontsize(8.5) 
    
def radiofunc(label):
    global filename
    filename = label
    update()
    '''
def checkfunc(label):
    global levels
    n = int(label[6:])
    if n in levels: levels.remove(n)
    else: levels.append(n)
    levels = sorted(levels)
    update()
    '''
def checkfunc(label):
    global levels,mode
    n = int(label[6:])
    if mode == "reconstruction":
        levels = range(-1, n+1)
    else:
        levels = [n]
    update()
    
def modesfunc(label):
    global mode, levels
    mode = label.lower()
    n = levels[-1]
    if mode == "reconstruction":
        levels = range(-1, n+1)
    else:
        levels = [n]
    update()
    
modes.on_clicked(modesfunc)
radio.on_clicked(radiofunc)
check.on_clicked(checkfunc)

plt.show()
