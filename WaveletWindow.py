from FourierWindow import *


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
    
	'''
        l = Label(self.leftPane, text='Wavelets')
        l.pack(fill=X, pady=(30,0), padx=5)

        dic = {'Haar':'haar', 'Daubechies':'db', 'Symlets':'sym', 'Coiflets':'coif', 
            'Biorthogonal':'bior', 'Reverse Biorthogonal':'rbio', 'Discrete Meyer':'dmey'}
        self.dic=dic
        self.family = StringVar()
        self.family.set('Daubechies')
        self.wavelet = StringVar()
        self.wavelet.set('db4')

        familyMenu = OptionMenu(self.leftPane, self.family, *dic.keys(), command=self.updateFamily)
        familyMenu.pack(fill=BOTH,pady=(0,0),padx=5)
        waveletMenu = OptionMenu(self.leftPane,self.wavelet, *pywt.wavelist(dic[self.family.get()]), command=(lambda x : self.updatePlots()))
        waveletMenu.pack(fill=BOTH, pady=(0,30),padx=5)
        
        self.waveletMenu=waveletMenu
    	'''
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        varNames = ['Max Scale']
        varLimits = [(1,512)]
        varRes = [1]
        varDTypes = [IntVar]
        varDefaults = [128]
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane((2,1), varValues)
        
        self.maxScale = self.vars[0]
        
    
    def updateFamily(self,_):
        self.waveletMenu['menu'].delete(0,'end')
        def c(val):
            self.wavelet.set(val)
            #print val
            self.updatePlots()

        for wavelet in pywt.wavelist(self.dic[self.family.get()]):
            #print wavelet
            self.waveletMenu['menu'].add_command(label=wavelet,command=lambda wavelet=wavelet:c(wavelet))

        self.wavelet.set(pywt.wavelist(self.dic[self.family.get()])[0])
        self.updatePlots()
    
    def wf(self, s_omega): # Mexican Hat

            a=s_omega**2
            b=s_omega**2/2
            return a* exp(-b)*2/(3**.5*pi**.25)   
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
        
        #if self.signalChanged: 
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
        plotcwt = abs(self.cwt)**2
        #plotcwt=clip(cwt, 0., 1000.)
        axes[1].cla()
        axes[1].imshow(plotcwt,aspect='auto')
        
        lines[0].set_data(t,data)
        axes[0].axis([0,len(data),min(data),max(data)])
        axes[1].axis([0,len(data),0,self.maxScale.get()])
        
        for axis in axes:
            axis.get_figure().canvas.draw_idle()
  
    
