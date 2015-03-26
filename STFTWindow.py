from FourierWindow import *
from scipy import signal

class STFTWindow(FourierWindow):
        
    def __init__(self, root):
        self.signalType = 0
    
        FourierWindow.__init__(self, root)
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        '''
        varTitles = ['Plot Type']
        varDTypes = [BooleanVar]
        varDefaults = [False]
        varTexts = [['Plot 2D', 'Plot 3D']]
        varVals = [[False, True]]
        
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        '''
        
        self._makeLeftPane(fileSelector=True)

        #self.plot3D = self.options[0]
        
        extraOptions = Frame(self.leftPane, bg='grey')
        extraOptions.grid(row=2, column=1, sticky=N+S+E+W)
        
        titlePane = Frame(extraOptions)
        titlePane.pack(fill=X, pady=(5,0), padx=5)
        
        Label(titlePane, text='Windows').pack(fill=BOTH, side=LEFT, expand=1)
        #Button(titlePane, text='?', command=self.popupWindow).pack(fill=BOTH, side=LEFT)

        dic = {'Modified Bartlett-Hann':'barthann', 'Bartlett':'bartlett', 'Blackman':'blackman', 'Blackman-Harris':'blackmanharris', 
        'Bohman':'bohman', 'Rectangular':'boxcar', 'Dolph-Chebyshev':'chebwin', 'Cosine':'cosine', 'Flat Top':'flattop', 'Hamming':'hamming',
        'Hann':'hann', 'Nutall':'nuttall', 'Parzen':'parzen', 'Triangular':'triang'}
        self.dic=dic
        self.window = StringVar()
        self.window.set('Rectangular')

        windowMenu = OptionMenu(extraOptions, self.window, *dic.keys(), command=(lambda x: self.updatePlots()))
        #windowMenu.config(width=20)
        windowMenu.pack(fill=BOTH,pady=(0,0),padx=5)
                
    def popupWindow(self):
        popup = Toplevel()
        fig = Figure(figsize=(5,5))
        ax0 = fig.add_subplot(211)
        ax1 = fig.add_subplot(212)

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.show()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        
        win = eval('signal.%s(%i)'%(self.dic[self.window.get()],self.width.get()))
        ax0.plot(win)
        self.formatAxes(ax0,range(self.width.get()),win,'Sample','Amplitude',self.window.get())
        
        F = np.fft.fftshift(abs(np.fft.fft(win,2048)))
        F = 10*np.log10(F[1024-40:1024+41])
        freqs = range(-len(F)/2,len(F)/2)
        ax1.plot(freqs,F)
        self.formatAxes(ax1,freqs,F,'FFT Bin','Decibels','Fourier Transform')
        
        fig.tight_layout()
    
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        varNames = ['Width', 'Center']
        varLimits = [(1,1024), (0,1024)]
        varRes = [1,1]
        varDTypes = [IntVar,IntVar]
        varDefaults = [10,0]
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane((2,2), varValues)
        
        self.width = self.vars[0]
        self.center = self.vars[1]
        

    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):        
        axes = self.axes
        lines = []
        dummy = [0]
        for axis in axes:
            l,=axis.plot(dummy)
            lines.append(l)
        l,=axes[0].plot(dummy, color='red')
        lines.append(l)
        self.lines = lines

        self.signalFromFile()

    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    
    def updatePlots(self):
        data = self.signal
        N = len(data)
        
        t = arange(N)
        delta_w = 1./(N-1)
        w = linspace(0, delta_w*(N/2-1), num=N/2)
        F = abs(fft.fft(data)[:N/2])
        
        width = self.width.get()
        center = self.center.get()
        
        #print width, center, (center-width/2), (N-center-width/2)
        win = eval('signal.%s(%i)'%(self.dic[self.window.get()],width))
        win = np.append(np.append([0]*N,win),[0]*N)
        win = win[N+width/2-center:2*N+width/2-center]
        
        win_data = win*data
        
        win_F = abs(fft.fft(win_data)[:N/2])
        
        lines = self.lines
        axes = self.axes
        
        lines[0].set_data(t,data)
        lines[4].set_data(t,win)
        lines[1].set_data(w,F)
        lines[2].set_data(t,win_data)
        lines[3].set_data(w,win_F)
        
        self.formatAxes(axes[0],t,data,'Time (sec)','Amplitude',self.filename.get())
        self.formatAxes(axes[1],w,F,'Frequency (Hz)','Magnitude','FFT of '+self.filename.get())
        self.formatAxes(axes[2],t,win_data,'Time (sec)','Amplitude','Windowed Signal')
        self.formatAxes(axes[3],w,win_F,'Frequency (Hz)','Magnitude','FFT of Windowed Signal')

        self.sliders[0][1].config(to=len(data)/2)
        self.sliders[1][1].config(to=len(data))
        
        for axis in axes:
            axis.get_figure().canvas.draw_idle()
        
if __name__ == "__main__":
    root = Tk()
    STFTWindow(root)
    root.mainloop()        

    
    
    
