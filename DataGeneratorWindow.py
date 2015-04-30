from FourierWindow import *
from scipy.signal import *

class DataGeneratorWindow(FourierWindow):
        
    def __init__(self, root):
        self.title = 'Data Generator'
        
        self.builtInFunctions = {'Sinusoid' : 'cos(f[0]*2*pi*t)',
                            'Two Sinusoids' : 'cos(f[0]*2*pi*t) + cos(f[1]*2*pi*t)',
                            'Two Seq. Sinusoids' : 'where(t<t[N/2], cos(f[0]*2*pi*t), cos(f[1]*2*pi*t))',
                            'Delta' : 'where(t==t[N/2], 1, 0)',
                            'Chirp' : 'sin((f[0]+(f[1]-f[0])/2*t/t[-1])*2*pi*t)'}
    
        N = 1024
        Fs = 10.
        Ts = 1/Fs
        self.maxFreqs=5
        t = linspace(0.,N*Ts,N)
        n = arange(N, dtype=float)
        freqs = (n / N * Fs) - (Fs / 2)
        self.params=[N,Fs,Ts,t,n,freqs]
    
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
        self.customFunc = StringVar()
        self.customFunc.set('sin(f0*t*cos(f1*t))')
        # variable for number of decaying complex exponentials
        self.numDCE = IntVar()
        self.numDCE.set(2)
        # boolean variable for exponential decay
        decay = BooleanVar()
        self.decay = decay
        decay.set(False)
        
        Label(leftPane, text='Functions').pack(fill=X, pady=(self.pads[1],0), padx=self.pads[0])
        # create a frame to hold the function radiobuttons
        funcFrame = Frame(leftPane)
        funcFrame.pack(fill=BOTH, padx=self.pads[0], pady=(0,self.pads[1]))
        
        
        # create all the radiobuttons
        for i in range(len(self.builtInFunctions)):
            text = self.builtInFunctions.keys()[i]
            f = Frame(funcFrame)
            f.pack(side=TOP, fill=BOTH)
            Radiobutton(f, text=text, variable=funcText, value=text, command=self.updatePlots).pack(side=LEFT)
        # custom function
        f = Frame(funcFrame)
        f.pack(side=TOP, fill=BOTH)
        Radiobutton(f, text='', variable=funcText, value='DCE', command=self.updatePlots).pack(side=LEFT)
        Entry(f, textvariable=self.numDCE, width=2).pack(side=LEFT)    
        Label(f, text='Decaying Complex Exponentials').pack(side=LEFT, fill=X)
        # custom function
        f = Frame(funcFrame)
        f.pack(side=TOP, fill=BOTH)
        Radiobutton(f, text='', variable=funcText, value='Custom', command=self.updatePlots).pack(side=LEFT)
        Entry(f, textvariable=self.customFunc).pack(side=LEFT)
        
        # create a frame to hold the exponential decay radiobuttons
        Label(leftPane, text='Exponential Decay').pack(fill=X, pady=(self.pads[1],0), padx=self.pads[0])
        expFrame = Frame(leftPane)
        expFrame.pack(fill=BOTH,pady=(0,self.pads[1]),padx=self.pads[0])
        # both radiobuttons
        Radiobutton(expFrame, text='Exponential Decay',variable=decay,value=True, 
            command=self.updatePlots).grid(row=0,stick=W,padx=self.pads[0])
        Radiobutton(expFrame, text='No Exponential Decay',variable=decay,value=False, 
            command=self.updatePlots).grid(row=1,stick=W,padx=self.pads[0])
            
        self.master.add(leftPane)
        
        b = Button(leftPane, text='Save Current Signal', command=self.file_save)
        b.pack(fill=BOTH, padx=self.pads[0], pady=self.pads[1])
    
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
        
        varNames = ['d%i'%i for i in range(self.maxFreqs)]
        varLimits = [(0, 0.05)]*self.maxFreqs
        varRes = [0.1]*self.maxFreqs
        varDTypes = [DoubleVar]*self.maxFreqs
        varDefaults = [1]*self.maxFreqs
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane((3,1),[varValues])
        
        self.freqs = self.vars[0]
        self.freqSliders = self.sliders[0]
      
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):
        self._initSignals()
        
        self.freqsUsed = range(self.maxFreqs)
    
    def parseSignal(self):     
        function = self.funcText.get()
        if function in self.builtInFunctions.keys():
            y = self.builtInFunctions[function]
        elif function == 'Custom':
            func = self.customFunc.get()
            for i in range(10): func = func.replace('f%i'%i, 'f[%i]'%i)
            y = func
        else:
            n = self.numDCE.get()
            t = ''
            for i in range(n):
                t += '1*exp(-0*t)*exp(1j*2*pi*f[%i]*t)+'%i
            y = t[:-1]
        self.function = y
    
    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    def updatePlots(self):
        [N,Fs,Ts,t,n,freqs] = self.params
        f = [self.freqs[i].get() for i in range(self.maxFreqs)]
        oldFreqs = self.freqsUsed
        newFreqs = []
        self.parseSignal()
        
        for slider in self.freqSliders:
            from_ = -10 if self.funcText.get() == 'DCE' else 0
            slider[1].config(from_=from_)

        for i in range(self.maxFreqs):
            if 'f[%i]'%i in self.function: newFreqs.append(i)
        self.hideShowFreqs(oldFreqs, newFreqs, self.freqSliders)
        self.freqsUsed = newFreqs
        
        y = eval(self.function)
        y = y.astype(np.complex_)
        if self.decay.get():
            y = y*exp(-0.03*t)       
        y /= max(np.abs(y)) 
        self.y = y
        S = abs(fft.fftshift(fft.fft(y)))
        
        self.lines[0].set_data(t,y)
        self.lines[1].set_data(freqs,S)
        
        funcName = self.funcText.get()
        if funcName in self.builtInFunctions.keys(): name = funcName
        else: name = self.customFunc.get()
        
        self.axes[2].cla()
        self.axes[2].specgram(y, Fs=Fs)#, NFFT=80, noverlap=40)
        #self.axes[2].axis([0, (N-128)*Ts, min(freqs), max(freqs)])
        
        self.formatAxes(self.axes[0],t,y,'Time (sec)','Normalized Amplitude',name)
        self.formatAxes(self.axes[1],freqs,S,'Frequency (Hz)','Magnitude','FFT of '+name)
        self.formatAxes(self.axes[2],t,freqs,'Time (sec)','Frequency (Hz)','Spectrogram, Fs = 10 Hz',spec=True)
        
        #for fig in self.figs:
        self.fig.canvas.draw_idle()
        self.fig.tight_layout()
        #[fig.canvas.draw_idle() for fig in self.figs]
        
        
if __name__ == "__main__":
    root = Tk()
    DataGeneratorWindow(root)
    
    if os.name == "nt": root.wm_state('zoomed')
    else: root.attributes('-zoomed', True)

    root.mainloop()
  
    
