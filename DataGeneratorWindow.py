from FourierWindow import *
from scipy.signal import *

class DataGeneratorWindow(FourierWindow):
        
    def __init__(self, root):
        self.title = 'Data Generator'
        
        self.builtInFunctions = {'Sinusoid' : 'cos(f[0]*2*pi*t)',
                            'Two Sinusoids' : 'cos(f[0]*2*pi*t) + cos(f[1]*2*pi*t)',
                            'Two Seq. Sinusoids' : 'where(t<t[N/2], cos(f[0]*2*pi*t), cos(f[1]*2*pi*t))',
                            'Delta' : 'where(t==t[N/2], 1, 0)',
                            'Chirp' : 'sin((f[0]+(f[1]-f[0])/2*t/t[-1])*2*pi*t)',
                            'Square': 'square(f[0]*2*pi*t)',
                            'Sqrt(Sinusoid)' : 'where(sin(2*pi*f[0]*t)>0, sqrt(sin(2*pi*f[0]*t)), 0.)',
                            'Sawtooth' : 'signal.sawtooth(f[0]*2*pi*t)'}
    
        N = 1024
        Fs = 1.
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
        
        Button(leftPane, text='Save Tables and Plots', command=self.saveScreenshot).pack(fill=X, pady=self.pads[1], padx=self.pads[0])
        
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
        # random noise
        noise = BooleanVar()
        self.noise = noise
        noise.set(False)
        # fft plot type
        fftPlot = BooleanVar()
        self.fftPlot = fftPlot
        fftPlot.set(False)
        
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
            
        # create a frame to hold the exponential decay radiobuttons
        Label(leftPane, text='Random Noise').pack(fill=X, pady=(self.pads[1],0), padx=self.pads[0])
        noiseFrame = Frame(leftPane)
        noiseFrame.pack(fill=BOTH,pady=(0,self.pads[1]),padx=self.pads[0])
        # both radiobuttons
        Radiobutton(noiseFrame, text='Add Noise',variable=noise,value=True, 
            command=self.updatePlots).grid(row=0,stick=W,padx=self.pads[0])
        Radiobutton(noiseFrame, text='No Noise',variable=noise,value=False, 
            command=self.updatePlots).grid(row=1,stick=W,padx=self.pads[0])
            
            # create a frame to hold the exponential decay radiobuttons
        Label(leftPane, text='FFT Plot Type').pack(fill=X, pady=(self.pads[1],0), padx=self.pads[0])
        noiseFrame = Frame(leftPane)
        noiseFrame.pack(fill=BOTH,pady=(0,self.pads[1]),padx=self.pads[0])
        # both radiobuttons
        Radiobutton(noiseFrame, text='Stem Plot',variable=fftPlot,value=True, 
            command=self.updatePlots).grid(row=0,stick=W,padx=self.pads[0])
        Radiobutton(noiseFrame, text='Normal Line Plot',variable=fftPlot,value=False, 
            command=self.updatePlots).grid(row=1,stick=W,padx=self.pads[0])
            
        self.master.add(leftPane)
        
        b = Button(leftPane, text='Save Current Signal', command=self.file_save)
        b.pack(fill=BOTH, padx=self.pads[0], pady=self.pads[1])
    
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        [N,Fs,Ts,t,n,freqs] = self.params
    
        freqNames = ['f%i'%i for i in range(self.maxFreqs)]
        freqLimits = [(Fs/100., Fs)]*self.maxFreqs
        freqRes = [Fs/100.]*self.maxFreqs
        freqDTypes = [DoubleVar]*self.maxFreqs
        freqDefaults = [1]*self.maxFreqs
        freqValues = [freqNames, freqLimits, freqRes, freqDTypes, freqDefaults]
        
        decayNames = ['T%i'%i for i in range(self.maxFreqs)]
        decayLimits = [(1, 1000)]*self.maxFreqs
        decayRes = [1]*self.maxFreqs
        decayDTypes = [IntVar]*self.maxFreqs
        decayDefaults = [100]*self.maxFreqs
        decayValues = [decayNames, decayLimits, decayRes, decayDTypes, decayDefaults]
        
        ampNames = ['A%i'%i for i in range(self.maxFreqs)]
        ampLimits = [(0, 100)]*self.maxFreqs
        ampRes = [1]*self.maxFreqs
        ampDTypes = [IntVar]*self.maxFreqs
        ampDefaults = [1]*self.maxFreqs
        ampValues = [ampNames, ampLimits, ampRes, ampDTypes, ampDefaults]
        
        phaseNames = ['p%i'%i for i in range(self.maxFreqs)]
        phaseLimits = [(0, 2*np.pi)]*self.maxFreqs
        phaseRes = [0.01]*self.maxFreqs
        phaseDTypes = [DoubleVar]*self.maxFreqs
        phaseDefaults = [0]*self.maxFreqs
        phaseValues = [phaseNames, phaseLimits, phaseRes, phaseDTypes, phaseDefaults]
        
        self._makeRightPane((3,1),[freqValues, decayValues, ampValues, phaseValues])
        
        self.freqs = self.vars[0]
        self.decays = self.vars[1]
        self.amps = self.vars[2]
        self.phases = self.vars[3]
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
                t += 'A[%i]*exp(-t/T[%i])*exp(1j*(2*pi*f[%i]*t+p[%i]))+'%(i,i,i,i)
            y = t[:-1]
        self.function = y
        
    def hideShowFreqs(self, oldFreqs, newFreqs, sliders):
        for i in oldFreqs + newFreqs:
            if i in oldFreqs:
                for k in range(len(sliders)):
                    sliders[k][i][0].grid_remove()
                    sliders[k][i][1].grid_remove()
            if i in newFreqs:
                for k in range(len(sliders)):
                    sliders[k][i][0].grid()
                    sliders[k][i][1].grid()

        if self.funcText.get() != 'DCE':
            for i in range(1,len(sliders)):
                for s in sliders[i]:
                    s[0].grid_remove()
                    s[1].grid_remove()
            
    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    def updatePlots(self):
        [N,Fs,Ts,t,n,freqs] = self.params
        f = [self.freqs[i].get() for i in range(self.maxFreqs)]
        T = [self.decays[i].get() for i in range(self.maxFreqs)]
        A = [self.amps[i].get() for i in range(self.maxFreqs)]
        p = [self.phases[i].get() for i in range(self.maxFreqs)]
        
        oldFreqs = self.freqsUsed
        newFreqs = []
        self.parseSignal()
        
        for slider in self.freqSliders:
            from_ = -Fs if self.funcText.get() == 'DCE' else 0
            slider[1].config(from_=from_)

        for i in range(self.maxFreqs):
            if 'f[%i]'%i in self.function: newFreqs.append(i)
        self.hideShowFreqs(oldFreqs, newFreqs, self.sliders)
        self.freqsUsed = newFreqs
        
        y = eval(self.function)
        y = y.astype(np.complex_)
        if self.decay.get() and self.funcText.get() != 'DCE':
            y = y*exp(-0.03*t)       
        y /= max(np.abs(y)) 
        
        if self.noise.get(): y += np.random.normal(scale=max(y)/10,size=len(y))
        
        self.y = y
        S = abs(fft.fftshift(fft.fft(y)))
        
        self.lines[0].set_data(t,y)
        self.axes[1].cla()
        self.axes[1].grid()
        if self.fftPlot.get():
            self.axes[1].stem(freqs,S,basefmt='k:')
        else:
            self.axes[1].plot(freqs,S)
            
        mean = sum([amp*freq for (freq, amp) in zip(freqs, S)])/sum(S)
        midpoint = sum(S)/2.
        cur = 0
        for ind in range(len(freqs)):
            cur += S[ind]
            if cur >= midpoint:
                median = freqs[ind]
                break
        stddev = (sum([(freq-mean)**2*amp for (freq,amp) in zip(freqs, S)])/sum(S))**0.5
        
        loc = [min(freqs) + (max(freqs)-min(freqs))*0.85, min(S) + (max(S)-min(S))*0.7]
        self.axes[1].text(loc[0],loc[1],'Mean: %0.5f\nMedian: %0.05f\nStd. Dev: %0.05f'%(mean,median,stddev),bbox={'facecolor':'white','alpha':1,'pad':10})
        
        
        funcName = self.funcText.get()
        if funcName in self.builtInFunctions.keys(): name = funcName
        elif funcName == 'Custom': name = self.customFunc.get()
        else: name = ''
        
        self.axes[2].cla()
        self.axes[2].specgram(y, Fs=Fs)#, NFFT=80, noverlap=40)
        #self.axes[2].axis([0, (N-128)*Ts, min(freqs), max(freqs)])
        
        self.formatAxes(self.axes[0],t,y,'Time (ms)','Normalized Amplitude',name)
        self.formatAxes(self.axes[1],freqs,S,'Frequency (kHz)','Magnitude','FFT of '+name)
        self.formatAxes(self.axes[2],t,freqs,'Time (ms)','Frequency (kHz)','Spectrogram, Fs = 10 kHz',spec=True)
        
        
        [ax.axhline(color='k') for ax in self.axes]
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
  
    
