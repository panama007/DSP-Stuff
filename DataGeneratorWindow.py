from FourierWindow import *
from scipy.signal import *

class DataGeneratorWindow(FourierWindow):
        
    def __init__(self, root):
        N = 1024
        Fs = 10.
        Ts = 1/Fs
        self.maxFreqs=5
        t = linspace(0.,N*Ts,N)
        n = arange(N, dtype=float)
        frequencies = (n / N * Fs)[:N/2]
        self.params=[N,Fs,Ts,t,n,frequencies]
    
        self.signalType = 0
    
        FourierWindow.__init__(self, root)     
        
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        leftPane = Frame(self.master, bg='grey')
        # create a variable to hold function currently being analyzed
        
        funcText = StringVar()
        self.funcText = funcText
        funcText.set('Sinusoid')
        
        # variable to hold the user-input function
        customFunc = StringVar()
        self.customFunc = customFunc
        customFunc.set('sin(f0*t*cos(f1*t))')
        # boolean variable for exponential decay
        decay = BooleanVar()
        self.decay = decay
        decay.set(False)
        
        Label(leftPane, text='Functions').pack(fill=X, pady=(15,0), padx=5)
        # create a frame to hold the function radiobuttons
        funcFrame = Frame(leftPane)
        funcFrame.pack(fill=BOTH, padx=5, pady=(0,15))
        
        
        # create all the radiobuttons
        for i in range(len(self.builtInFunctions)):
            text = self.builtInFunctions.keys()[i]
            rb = Radiobutton(funcFrame, text=text, variable=funcText, value=text, command=self.updatePlots)
            rb.grid(row=i,columnspan=2,sticky=W,padx=(5,0))
        # custom function radiobutton
        rb = Radiobutton(funcFrame, text='', variable=funcText, value=' ', command=self.updatePlots)
        rb.grid(row=5,sticky=W,padx=(5,0))
        # custom function text entry box
        eb = Entry(funcFrame, textvariable=customFunc)
        eb.grid(row=5,column=1,sticky=E,padx=(0,5))
        
        # create a frame to hold the exponential decay radiobuttons
        Label(leftPane, text='Exponential Decay').pack(fill=X, pady=(15,0), padx=5)
        expFrame = Frame(leftPane)
        expFrame.pack(fill=BOTH,pady=(0,15),padx=5)
        # both radiobuttons
        Radiobutton(expFrame, text='Exponential Decay',variable=decay,value=True, 
            command=self.updatePlots).grid(row=0,stick=W,padx=5)
        Radiobutton(expFrame, text='No Exponential Decay',variable=decay,value=False, 
            command=self.updatePlots).grid(row=1,stick=W,padx=5)
            
        self.master.add(leftPane)
        
        b = Button(leftPane, text='Save Current Signal', command=self.file_save)
        b.pack(fill=BOTH, padx=5, pady=15)
    
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        varNames = ['f%i'%i for i in range(self.maxFreqs)]
        varLimits = [(0.1, 10)]*self.maxFreqs
        varRes = [0.1]*self.maxFreqs
        varDTypes = [DoubleVar]*self.maxFreqs
        varDefaults = [1]*self.maxFreqs
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane((3,1),varValues)
        
        self.frequencies = self.vars
        self.frequencySliders = self.sliders
      
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):
        [N,Fs,Ts,t,n,frequencies]=self.params
        self.function=self.builtInFunctions[self.funcText.get()]
        self.freqsUsed = range(self.maxFreqs)
        
        y = sin(1.*2*pi*t)
        if self.decay.get():
            y = y*exp(-0.03*t)
        
        S = fft.fft(y)
        S = abs(fft.fftshift(S))[N/2:]
        
        axes = self.axes
        lines = [0]*2
        self.lines = lines

        lines[0], = axes[0].plot(t,y)
        self.formatAxes(axes[0],t,y,'Time (sec)','Normalized Amplitude',self.funcText.get())

        lines[1], = axes[1].plot(frequencies,S)
        self.formatAxes(axes[1],frequencies,S,'Frequency (Hz)','Amplitude','FFT of Signal')

        axes[2].specgram(y, Fs=Fs, NFFT=80, noverlap=40)
        axes[2].axis([0, (N-128)*Ts, 0, 2*pi])
        self.formatAxes(axes[2],t,frequencies,'Time (sec)','Frequency (Hz)','Spectrogram',spec=True)
        
        for axis in axes:
            axis.get_figure().canvas.draw_idle()
    
    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    def updatePlots(self):
        [N,Fs,Ts,t,n,frequencies] = self.params
        f = [self.frequencies[i].get() for i in range(self.maxFreqs)]
        oldFreqs = self.freqsUsed
        newFreqs = []
        self.parseSignal() 
        for i in range(self.maxFreqs):
            if 'f[%i]'%i in self.function: newFreqs.append(i)
        self.hideShowFreqs(oldFreqs, newFreqs)
        self.freqsUsed = newFreqs
        
        y = eval(self.function)
        if self.decay.get():
            y = y*exp(-0.03*t)       
        y /= max(y) 
        self.y = y
        S = abs(fft.fftshift(fft.fft(y)))[N/2:]
        
        self.lines[0].set_ydata(y)
        self.lines[1].set_ydata(S)
        
        funcName = self.funcText.get()
        if funcName in self.builtInFunctions.keys(): name = funcName
        else: name = self.customFunc.get()
        
        self.axes[0].set_title(name)
        self.axes[1].set_title('FFT of '+name)
        self.axes[1].axis([0,Fs/2,min(S),max(S)])
        
        self.axes[2].cla()
        self.axes[2].specgram(y, Fs=Fs, NFFT=80, noverlap=40)
        self.axes[2].axis([0, (N-128)*Ts, min(frequencies), max(frequencies)])
        self.formatAxes(self.axes[2],t,frequencies,'Time (sec)','Frequency (Hz)','Spectrogram',spec=True)
        
        for fig in self.figs:
            fig.tight_layout()
        for axis in self.axes:
            axis.get_figure().canvas.draw_idle()
        
        
if __name__ == "__main__":
    root = Tk()
    DataGeneratorWindow(root)
    root.mainloop()
  
    
