from FourierWindow import *
from scipy.signal import *

class DataGeneratorWindow(FourierWindow):
        
    def __init__(self, root):
        self.title = 'Data Generator'
        
        self.builtInFunctions = {'Sinusoid' : 'sin(f[0]*2*pi*t)',
                            'Two Sinusoids' : 'sin(f[0]*2*pi*t) + sin(f[1]*2*pi*t)',
                            'Two Seq. Sinusoids' : 'where(t<t[N/2], sin(f[0]*2*pi*t), sin(f[1]*2*pi*t))',
                            'Delta' : 'where(t==t[N/2], 1, 0)',
                            'Chirp' : 'sin((f[0]+(f[1]-f[0])/2*t/t[-1])*2*pi*t)'}
    
        N = 1024
        Fs = 10.
        Ts = 1/Fs
        self.maxFreqs=5
        t = linspace(0.,N*Ts,N)
        n = arange(N, dtype=float)
        freqs = (n / N * Fs)[:N/2]
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
        customFunc = StringVar()
        self.customFunc = customFunc
        customFunc.set('sin(f0*t*cos(f1*t))')
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
            rb = Radiobutton(funcFrame, text=text, variable=funcText, value=text, command=self.updatePlots)
            rb.grid(row=i,columnspan=2,sticky=W,padx=(self.pads[0],0))
        # custom function radiobutton
        rb = Radiobutton(funcFrame, text='', variable=funcText, value=' ', command=self.updatePlots)
        rb.grid(row=5,sticky=W,padx=(self.pads[0],0))
        # custom function text entry box
        eb = Entry(funcFrame, textvariable=customFunc)
        eb.grid(row=5,column=1,sticky=E,padx=(0,self.pads[0]))
        
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
        
        self._makeRightPane((3,1),varValues)
        
        self.freqs = self.vars
        self.freqSliders = self.sliders
      
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):
        self._initSignals()
        
        self.freqsUsed = range(self.maxFreqs)
    
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
        for i in range(self.maxFreqs):
            if 'f[%i]'%i in self.function: newFreqs.append(i)
        self.hideShowFreqs(oldFreqs, newFreqs, self.freqSliders)
        self.freqsUsed = newFreqs
        
        y = eval(self.function)
        if self.decay.get():
            y = y*exp(-0.03*t)       
        y /= max(np.abs(y)) 
        self.y = y
        S = abs(fft.fftshift(fft.fft(y)))[N/2:]
        
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
        
        for fig in self.figs:
            fig.canvas.draw_idle()
            fig.tight_layout()
        #[fig.canvas.draw_idle() for fig in self.figs]
        
        
if __name__ == "__main__":
    root = Tk()
    DataGeneratorWindow(root)
    
    if os.name == "nt": root.wm_state('zoomed')
    else: root.attributes('-zoomed', True)

    root.mainloop()
  
    
