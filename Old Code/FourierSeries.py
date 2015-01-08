import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.widgets import Slider, Button, RadioButtons

gibbs = 0
max_terms = 500

class Function:
    def __init__(self, func, range, period, text):
        self.func = func
        self.range = range
        self.period = period
        self.text = text
        

f1 = Function(lambda x: np.where(np.sin(x)>0, np.sqrt(np.sin(x)), 0.), (-0.5, 1.5), 2*np.pi, r'$f_1(x)=\sqrt{sin(x)}$')
f2 = Function(lambda x: np.where(np.abs(np.mod(x-1,2)) < 1, np.mod(x-1,2), -1), (-1.5, 1.5), 2, '$f_2(x)= x-1 \ \ mod\ \ 2$\n  $-1\ : x\in[2n,2n+1]$')

#@memoize
def cn(x, y, n, period):
    c = y * np.exp(-1j * 2. * np.pi * n * x / period)
    return c.sum()/c.size
    
#@memoize
def fSeries(x, y, Nh, period):
    global gibbs
    rng = np.arange(0., Nh)
    coeffs = np.array([cn(x,y,i,period) for i in rng])
    if gibbs:
        f = np.array([(2. if i>0 else 1.) * coeffs[i] * np.sinc(i*np.pi/(2*Nh)) * np.exp(1j*2*i*np.pi*x/period) for i in rng])
    else:
        f = np.array([(2. if i>0 else 1.) * coeffs[i] * np.exp(1j*2*i*np.pi*x/period) for i in rng])
    return f.sum(axis=0)

    
fig, ((ax, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
plt.subplots_adjust(left=0.30, bottom=0.2, right=0.95, top=0.93)

n0 = 1
f0 = 3

function = f1
period, range = function.period, function.range

x = np.arange(-2*period, 2*period, 0.001)
s = function.func(x)
l, = ax.plot(x,s, lw=2, color='red')
S = fSeries(x, s, n0, period).real
l2, = ax3.plot(x, S, lw=2, color='red')
coeffs = np.array([cn(x,s,i,period) for i in np.arange(n0)])
ax2.stem(coeffs.real, basefmt='k-')
ax4.stem(-coeffs.imag, basefmt='k-')

ax.axis([-2*period, 2*period, range[0], range[1]])
ax3.axis([-2*period, 2*period, range[0], range[1]])

ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')
ax3.spines['bottom'].set_position('zero')
ax3.spines['left'].set_position('zero')
ax2.spines['bottom'].set_position('zero')
ax2.spines['left'].set_position('zero')
ax4.spines['bottom'].set_position('zero')
ax4.spines['left'].set_position('zero')

ax.set_title("Fourier Series Example", fontsize=12)
ax2.set_title("Fourier Series Coefficients", fontsize=12)

ax.set_ylabel("Original Signal", fontsize=10)
ax3.set_ylabel("Fourier Series Approximation", fontsize=10)
ax2.set_ylabel("Cosine Coefficients", fontsize=10)
ax4.set_ylabel("Sine Coefficients", fontsize=10)

ax.yaxis.set_label_coords(-0.05,0.5)
ax3.yaxis.set_label_coords(-0.05,0.5)
ax2.yaxis.set_label_coords(-0.05,0.5)
ax4.yaxis.set_label_coords(-0.05,0.5)

axcolor = 'white'

axNum  = plt.axes([0.30, 0.1, 0.65, 0.03], axisbg=axcolor)

sNum = Slider(axNum, 'Num. Terms', 0, max_terms, valinit=n0, valfmt='%i')


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
    


def update(val):

    n = int(sNum.val)

    period, range = function.period, function.range
    
    x = np.arange(-2*period, 2*period, 0.001)
    
    s = function.func(x)
    S = fSeries(x, s, n, period).real
    l.set_xdata(x)
    l.set_ydata(s)
    l2.set_xdata(x)
    l2.set_ydata(S)
    coeffs = np.array([cn(x,s,i,period) for i in np.arange(n)])

    clear_axis(ax2)
    clear_axis(ax4)
    
    ax2.stem(coeffs.real, basefmt='k-')
    ax4.stem(-coeffs.imag, basefmt='k-')
    
    cos_coeff_range = np.max(coeffs.real) - np.min(coeffs.real)
    sin_coeff_range = np.max(-coeffs.imag) - np.min(-coeffs.imag)
    
    ax.axis([-2*period, 2*period, range[0], range[1]])
    ax3.axis([-2*period, 2*period, range[0], range[1]])
    ax2.axis([-0.5, n+0.5, np.min(coeffs.real)-0.1*cos_coeff_range, np.max(coeffs.real)+0.1*cos_coeff_range])
    ax4.axis([-0.5, n+0.5, np.min(-coeffs.imag)-0.1*sin_coeff_range, np.max(-coeffs.imag)+0.1*sin_coeff_range])
    
    fig.canvas.draw_idle()
    
    
sNum.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    sNum.reset()
button.on_clicked(reset)

rc('text', usetex=True)
rax = plt.axes([0.025, 0.5, 0.24, 0.15], axisbg=axcolor)
rGibbs = plt.axes([0.025, 0.3, 0.24, 0.12], axisbg=axcolor)


radio = RadioButtons(rax, (f1.text, f2.text), active=0)
radio2 = RadioButtons(rGibbs, ("Gibb's Effect Correction", "none"), active=1)

for label in radio2.labels:
    label.set_fontsize(8.5) 
    
def radiofunc(label):
    global function
    function = f1 if label == f1.text else f2
    update(0)
def radioGibbs(label):
    global gibbs
    if label == "Gibb's Effect Correction": gibbs = 1
    else: gibbs = 0
    update(0)
radio.on_clicked(radiofunc)
radio2.on_clicked(radioGibbs)

plt.show()
