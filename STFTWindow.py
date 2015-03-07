from FourierWindow import *

class STFTWindow(FourierWindow):
        
    def __init__(self, root):
        self.folder = 'signals2/'
        self.filenames = os.listdir(self.folder)
    
        FourierWindow.__init__(self, root)
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
    
        varDTypes = [StringVar, BooleanVar]
        varDefaults = [self.windows[0], False]
        varTexts = [self.windows, ['Plot 2D', 'Plot 3D']]
        varVals = [self.windows, [False, True]]
        
        optionsSpecs = [varDTypes, varDefaults, varTexts, varVals]
        
        
        self._makeLeftPane(optionsSpecs, True)
        
        self.window = self.options[0]
        self.mode = self.options[1]
    
    
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        varNames = ['Std. Dev.', 'Center']
        varLimits = [(10,50), (0,200)]
        varRes = [0.1,0.1]
        varDTypes = [DoubleVar,DoubleVar]
        varDefaults = [10,0]
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane(4, varValues)
        
        self.stdDev = self.vars[0]
        self.center = self.vars[1]
        
    def wf(self, s_omega): # Mexican Hat

            a=s_omega**2
            b=s_omega**2/2
            return a* exp(-b)/1.1529702    
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):        
        lines = [0]*1
        self.lines = lines
        axes = self.axes
        
        dummy = [0]
        lines[0], = axes[0].plot(dummy)
        
        self.formatAxes(axes[0],dummy,dummy,'Time (sec)','Amplitude','Original Signal')
        self.formatAxes(axes[1],dummy,dummy,'Time (sec)','Scale','Scalogram')
        
        self.signalFromFile()

    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    
    def updatePlots(self):
        data = self.signal
        M = len(data)
        t = arange(M)
        
        if self.signalChanged: 
            self.cwt= zeros((self.maxScale.get(),M), complex64)
            omega= array(range(0,M/2)+range(-M/2,0))*(2.0*pi/M)
            datahat=fft.fft(data)


            for scale in range(self.maxScale.get()):
                s_omega = omega*scale
                psihat=self.wf(s_omega)
                psihat = psihat *  sqrt(2.0*pi*scale)
                convhat = psihat * datahat
                W    = fft.ifft(convhat)
                self.cwt[scale,0:M] = W     
            
        self.signalChanged = False
        
        axes = self.axes       
        lines = self.lines
                
        # 2-d coefficient plot
        plotcwt = abs(self.cwt)
        #plotcwt=clip(cwt, 0., 1000.)
        axes[1].cla()
        axes[1].imshow(plotcwt,aspect='auto')
        
        lines[0].set_data(t,data)
        axes[0].axis([0,len(data),min(data),max(data)])
        axes[1].axis([0,len(data),0,self.maxScale.get()])
        
        for axis in axes:
            axis.get_figure().canvas.draw_idle()
  
        

    
    
    
