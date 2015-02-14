#from pywt import *

from FourierWindow import *
from helper_functions import *

class WaveletWindow(FourierWindow):
        
    def __init__(self, root):
        self.folder = 'signals/'
        self.filenames = os.listdir(self.folder)
    
        FourierWindow.__init__(self, root)
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        
        self._makeLeftPane(fileSelector=True) 
    
    
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        varNames = ['Max Scale', 'Mult']
        varLimits = [(1,512), (0.01,5)]
        varRes = [1,0.01]
        varDTypes = [IntVar,DoubleVar]
        varDefaults = [128,1]
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane(2, varValues)
        
        self.maxScale = self.vars[0]
        
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
  
    
