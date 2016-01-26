from FourierWindow import *


class FSeriesWindow(FourierWindow):
        
    def __init__(self, root):
        self.title = 'Fourier Series'
    
        self.maxTerms=100
        
        self.signalType = 0
    
        FourierWindow.__init__(self, root)
  
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        self.dic = {'sqrt(sin(x))': (lambda x: np.where(np.sin(2*pi*x)>0, np.sqrt(np.sin(2*pi*x)), 0.)), 
                    'f2' : (lambda x: np.where(signal.sawtooth(2*pi*x)>0, signal.sawtooth(2*pi*x), -1)),
                    'Square' : (lambda x: signal.square(2*pi*x)), 'Sawtooth' : (lambda x: signal.sawtooth(2*pi*x))}
    
        varTitles = ['Function',"Gibb's Effect Correction"]
        varDTypes = [StringVar, BooleanVar]
        varDefaults = [self.dic.keys()[0], False]
        varTexts = [self.dic.keys(),['None', 'Yes']]
        varVals = [self.dic.keys(), [False,True]]

        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        self._makeLeftPane(optionsSpecs)
        
        self.funcText = self.options[0]
        self.gibbs = self.options[1]
    
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        varNames = ['Num. Terms']
        varLimits = [(0,self.maxTerms)]
        varRes = [1]
        varDTypes = [IntVar]
        varDefaults = [1]
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane((2,2), [varValues])
        
        self.numTerms = self.vars[0][0]
        
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):
        self._initSignals()
        
    def cn(self, x, y, n, period):
        c = y * np.exp(-1j * 2. * np.pi * n * x / period)
        return c.sum()/c.size
        
    def fSeries(self, x, y, Nh, period):
        rng = np.arange(0., Nh)
        coeffs = np.array([self.cn(x,y,i,period) for i in rng])
        if self.gibbs.get():
            f = np.array([(2. if i>0 else 1.) * coeffs[i] * np.sinc(i*np.pi/(2*Nh)) * np.exp(1j*2*i*np.pi*x/period) for i in rng])
        else:
            f = np.array([(2. if i>0 else 1.) * coeffs[i] * np.exp(1j*2*i*np.pi*x/period) for i in rng])
        return coeffs, f.sum(axis=0)
    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    #TODO keep variable of FFT of each level so don't have to compute each time
    def updatePlots(self):
        funcText = self.funcText.get()
        func = self.dic[funcText]
        
        dt = 4./1024
        t = np.linspace(-2,2-dt,1024)
        y = func(t)
        #print sum(y)/len(t), t[0], t[-1]
        n = self.numTerms.get()
        
        coeffs, approx = self.fSeries(t,y,n,1.)
        
        self.axes[2].cla()
        self.axes[2].grid()
        self.axes[3].cla()
        self.axes[3].grid()
        
        self.lines[0].set_data(t,y)
        self.lines[1].set_data(t,approx)
        self.axes[2].stem(coeffs.real,basefmt='k:')
        self.axes[3].stem(-coeffs.imag,basefmt='k:')

        self.formatAxes(self.axes[0],t,y,'Time (ms)','Amplitude',funcText)
        self.formatAxes(self.axes[1],t,approx,'Time (ms)','Amplitude','Approximation of '+funcText)
        self.formatAxes(self.axes[2],range(-1,n+1),coeffs.real,'Frequency (kHz)','Coefficient','Cosine Coefficients')
        self.formatAxes(self.axes[3],range(-1,n+1),-coeffs.imag,'Frequency (kHz)','Coefficient','Sine Coefficients')
        
        if max(coeffs.real) < 0: self.axes[2].set_ylim([self.axes[2].get_ylim()[0], 0])
        if min(coeffs.real) > 0: self.axes[2].set_ylim([0, self.axes[2].get_ylim()[1]])
        if max(-coeffs.imag) < 0: self.axes[3].set_ylim([self.axes[3].get_ylim()[0], 0])
        if min(-coeffs.imag) > 0: self.axes[3].set_ylim([0, self.axes[3].get_ylim()[1]])
        
        [ax.axhline(color='k') for ax in self.axes]
        #for fig in self.figs:
        self.fig.canvas.draw_idle()
        self.fig.tight_layout()
            #fig.tight_layout()
        
if __name__ == "__main__":
    root = Tk()
    FSeriesWindow(root)
    
    if os.name == "nt": root.wm_state('zoomed')
    else: root.attributes('-zoomed', True)

    root.mainloop()  
    
