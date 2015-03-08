from FourierWindow import *
from wavelets import *


class WaveletWindow(FourierWindow):
        
    def __init__(self, root):
        self.signalType = 0
        
        self.cwt = {}
        self.plot3D = 0
    
        FourierWindow.__init__(self, root)
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        
        varTitles = ['Plot Type']
        varDTypes = [IntVar]
        varDefaults = [0]
        varTexts = [['Plot 2D', 'Plot 3D', 'Contour Plot']]
        varVals = [range(3)]
        
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        self._makeLeftPane(optionsSpecs, True) 
        self.plotType = self.options[0]
        
	
        l = Label(self.leftPane, text='Wavelets')
        l.pack(fill=X, pady=(30,0), padx=5)

        dic = {'Mexican Hat':'mexh'}#, 'Morlet':'morl', 'Haar':'haar', 'Daubechies':'db', 'Symlets':'sym', 'Coiflets':'coif', 
            #'Biorthogonal':'bior', 'Reverse Biorthogonal':'rbio', 'Discrete Meyer':'dmey'}
        self.dic=dic
        self.family = StringVar()
        self.family.set('Mexican Hat')#'Daubechies')
        self.wavelet = StringVar()
        self.wavelet.set('mexh')#'db4')

        if self.family.get() == 'Mexican Hat' or self.family.get() == 'Morlet':
            wavelets = [self.dic[self.family.get()]]
        else:
            wavelets = pywt.wavelist(self.dic[self.family.get()])
        
        familyMenu = OptionMenu(self.leftPane, self.family, *dic.keys(), command=self.updateFamily)
        familyMenu.pack(fill=BOTH,pady=(0,0),padx=5)
        waveletMenu = OptionMenu(self.leftPane,self.wavelet, *wavelets, command=(lambda x : self.updatePlots()))
        waveletMenu.pack(fill=BOTH, pady=(0,30),padx=5)
        
        self.waveletMenu=waveletMenu
    	
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

            self.updatePlots()
        if self.family.get() == 'Mexican Hat' or self.family.get() == 'Morlet':
            wavelets = [self.dic[self.family.get()]]
        else:
            wavelets = pywt.wavelist(self.dic[self.family.get()])
        
        for wavelet in wavelets:

            self.waveletMenu['menu'].add_command(label=wavelet,command=lambda wavelet=wavelet:c(wavelet))

        self.wavelet.set(wavelets[0])
        self.updatePlots()
    
  
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):        
        lines = [0]*2
        self.lines = lines
        axes = self.axes
        
        dummy = [0]
        
        lines[0], = axes[0].plot(dummy)
        lines[1] = axes[1].imshow([[0]*1024 for i in range(128)])
        
        #self.formatAxes(axes[0],dummy,dummy,'Time (sec)','Amplitude','Original Signal')
        #self.formatAxes(axes[1],dummy,dummy,'Time (sec)','Scale','Scalogram')
        
        self.signalFromFile()

    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    
    def updatePlots(self):
        data = self.signal
        M = len(data)
        t = arange(M)
        name = self.filename.get()

        
        if self.family.get() == 'Mexican Hat' or self.family.get() == 'Morlet':
            wave = eval(self.wavelet.get())
        else:
            wave = (lambda x,y: other(x,y,self.wavelet.get()))
        
        if (name,wave) not in self.cwt.keys(): self.cwt[(name,wave)] = signal.cwt(data, wave, arange(1,self.maxScale.get()+1))
        elif len(self.cwt[(name,wave)]) < self.maxScale.get(): 

            new = signal.cwt(data, wave, arange(len(self.cwt[(name,wave)])+1, self.maxScale.get()+1))
            self.cwt[(name,wave)] = np.append(self.cwt[(name,wave)], new, axis=0)

        self.signalChanged = False
        
        axes = self.axes       
        figs = self.figs
        lines = self.lines
                

        plotcwt = abs(self.cwt[(name,wave)][:self.maxScale.get()])#**2

        figs[1].clf()
        if self.plotType.get() == 0:
            axes[1] = figs[1].add_subplot(111)

            
            axes[1].imshow(plotcwt,aspect='auto')
        elif self.plotType.get() == 2:
            axes[1] = figs[1].add_subplot(111)


            axes[1].contour(plotcwt)
        else:
            axes[1] = figs[1].add_subplot(111, projection='3d')


            shape = plotcwt.shape
            Y = np.array([range(shape[0]) for i in range(shape[1])]).T
            X = np.array([[i]*shape[0] for i in range(shape[1])]).T

            self.plot3D = axes[1].plot_surface(X ,Y,plotcwt,cmap=matplotlib.cm.jet)

        
        lines[0].set_data(t,data)
        axes[0].axis([0,len(data),min(data),max(data)])
        axes[1].axis([0,len(data),0,self.maxScale.get()])
        
        self.formatAxes(axes[0],t,data,'Time (sec)','Amplitude','Original Signal')
        self.formatAxes(axes[1],t,range(self.maxScale.get()),'Frequency','Scale','Scalogram of Original Signal')
        
        for axis in axes:
            axis.get_figure().canvas.draw_idle()
  
    
