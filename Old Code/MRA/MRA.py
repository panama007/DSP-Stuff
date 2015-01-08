import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
from helper_functions import *

file_name = 'G31722.dat'
levels = range(-1,8)
N = 8
    
fig, (ax,ax2) = plt.subplots(nrows=2, ncols=1)
plt.subplots_adjust(left=0.30, bottom=0.1, right=0.95, top=0.93)

f = np.loadtxt(file_name)
f = f[:256]

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

ax.set_title("Signal", fontsize=12)
ax2.set_title("Fourier Transform", fontsize=12)

ax.set_ylabel("Amplitude", fontsize=10)
ax2.set_ylabel("Amplitude", fontsize=10)

ax.yaxis.set_label_coords(-0.05,0.5)
ax2.yaxis.set_label_coords(-0.05,0.5)

axcolor = 'white'


def update(val):
    print levels
    print 1
    f = np.loadtxt(file_name)
    f = f[:256]
    (A, a) = mra(f, N)
    print 2
    #print A[0]
    
    s = np.zeros(len(f))
    for i in levels:
        s += A[i+1]
    print 3
        
    FF = np.abs(fft(s)[:NN])   
    print 4
    l.set_ydata(s)
    print 5
    l2.set_ydata(FF)
    print 6
    #print "got here"
    
    ax.axis([0, M, min(s), max(s)])
    ax2.axis([min(w), max(w), min(FF), max(FF)])
    
    fig.canvas.draw_idle()
    print 7


#rc('text', usetex=True)
rax = plt.axes([0.025, 0.5, 0.15, 0.10], axisbg=axcolor)
rCheck = plt.axes([0.025, 0.2, 0.15, 0.2], axisbg=axcolor)


radio = RadioButtons(rax, ('G31722.dat', 'chirp.dat', 'SINUS12.dat', 'SINUS12B.dat'), active=0)
check = CheckButtons(rCheck, ["Level "+str(i) for i in range(-1,8)], (True,True,True,True,True,True,True,True, True))

for label in radio.labels + check.labels:
    label.set_fontsize(8.5) 
    
def radiofunc(label):
    global file_name
    file_name = label
    update(0)
def checkfunc(label):
    global levels
    n = int(label[6:])
    if n in levels: levels.remove(n)
    else: levels.append(n)
    levels = sorted(levels)
    update(0)
radio.on_clicked(radiofunc)
check.on_clicked(checkfunc)

plt.show()
