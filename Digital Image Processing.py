import numpy as np									                            # contains numerical computation functions
import matplotlib
matplotlib.use('TkAgg')
import Tkinter as Tk
from matplotlib.widgets import Slider, Button, RadioButtons	# contains sliders/buttons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from PIL import Image

def create_filter(N, r1, r2, filter_type):
    f = np.zeros((N,N), dtype=int)
    for x in range(N):
        for y in range(N):
            r = (x-N/2)**2+(y-N/2)**2
            if filter_type == "lowpass":
                f[x][y] = 1*(r<r1**2)
            if filter_type == "highpass":
                f[x][y] = 1*(r>=r1**2)
            if filter_type == "bandpass":
                f[x][y] = 1*(r<r2**2 and r>=r1**2)
    return f

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
    ax.xaxis.set_label_coords(0.5,-0.05)

filenames = os.listdir("images/")                                             # different images
imag = matplotlib.image.imread("images/"+filenames[0])
global fil, fil_type
fil_type = "lowpass"
#imag = Image.open("images/"+filenames[0])

root = Tk.Tk()
root.wm_title('Digital Image Processing')

#Create a toplevel menu (for selecting matrices)
menubar = Tk.Menu(root)

#Create the Matrix pulldown menu, and add it to the menubar
"""filemenu = Tk.Menu(menubar,tearoff=0)
for i, image in enumerate():
    expression = \
    'filemenu.add_command(label=mat,command=lambda: selectMatrix({}))'.format(i)
    eval(expression)
menubar.add_cascade(label="Select Matrix",menu=filemenu)

#Display the menu
root.config(menu=menubar)
"""
#Create a figure and an axes within it
fig = matplotlib.figure.Figure()
ax = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
fig.subplots_adjust(left=0.30, bottom=0.22, right=0.95, top=0.93, hspace=0.45)  # sets the spacing limits on the 4 plots

# a tk drawing area
canvas = FigureCanvasTkAgg(fig,master=root)#no resize callback as of now
canvas.get_tk_widget().pack(side=Tk.BOTTOM)




axR1 = fig.add_axes([0.30, 0.1, 0.63, 0.03])         # creates the sliders for adjusting the window
axR2 = fig.add_axes([0.30, 0.06, 0.63, 0.03])

sliderR1 = Slider(axR1, 'Radius 1', 0, 100, valinit=20, valfmt='%i')   # adds label, sets initial value, sets range for sliders
sliderR2 = Slider(axR2, 'Radius 2', 0, 100, valinit=20, valfmt='%i')

rax = fig.add_axes([0.025, 0.5, 0.22, 0.15])                  # creates the box for selecting a window
rax.set_title("Filters")
radio = RadioButtons(rax, ("Bandpass", "Lowpass", "Highpass"), active=1)

def update(val):
    global fil, fil_type
    r1 = int(sliderR1.val)
    r2 = int(sliderR2.val)
    fil = create_filter(len(imag), r1, r2, fil_type)
    #print "Entered update, r1 = %i, r2 = %i, type = %s"%(r1,r2,fil_type)
    
    imag_freq = np.fft.fft2(imag)
    imag_freq = np.fft.fftshift(imag_freq)
    
    filtered_imag = abs(np.fft.ifft2(np.fft.ifftshift(fil*imag_freq)))
    
    clear_axis(ax3)
    clear_axis(ax4)
    
    ax3.imshow(fil, cmap='gray', vmin=0, vmax=1, origin='lower')
    ax4.imshow(filtered_imag, cmap='gray', vmin=0, vmax=255, origin='lower')
    
    fig.canvas.draw_idle() 
sliderR1.on_changed(update)
sliderR2.on_changed(update)


def radiofunc(label):                                                                     # function to be run when a different filter is selected
    global fil_type 
    fil_type = label.lower()
    update(0)                                                                                # updates the plots since we changed the window
radio.on_clicked(radiofunc)                                                            # attaches the "radiofunc" to our radio buttons.
    

ax.imshow(imag,cmap='gray',vmin=0,vmax=255,origin='lower')
ax.set_title("Image")

imag_freq = np.fft.fft2(imag)
#imag_freq /= imag_freq.max()
#imag_freq = 1 - imag_freq
imag_freq = np.fft.fftshift(imag_freq)
imag_freq2 = abs(imag_freq)
imag_freq2 = np.log10(imag_freq2)
ax2.imshow(imag_freq2,cmap='gray',origin='lower')
ax2.set_title("2D FFT of Image")

fil = create_filter(512,20,0,"lowpass")
ax3.imshow(fil, cmap='gray', vmin=0, vmax=1)
ax3.set_title("2D FFT of Filter")

filtered_imag = abs(np.fft.ifft2(np.fft.ifftshift(fil*imag_freq)))
ax4.imshow(filtered_imag, cmap='gray', origin='lower', vmin=0,vmax=255)
ax4.set_title("Filtered Image")

#Draw the plot on the canvas
canvas.show()

Tk.mainloop()
