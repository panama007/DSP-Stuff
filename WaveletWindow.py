from FourierWindow import *
from wavelets2 import *


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
        
        varTitles = ['Plot Type', 'Contour Color']
        varDTypes = [IntVar, IntVar]
        varDefaults = [0, 0]
        varTexts = [['Plot 2D', 'Plot 3D', 'Contour Plot'], ['Color', 'Grayscale']]
        varVals = [range(3), range(2)]
        
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        self._makeLeftPane(optionsSpecs, True) 
        self.plotType = self.options[0]
        self.contourColor = self.options[1]
        
        extraOptions = Frame(self.leftPane, bg='grey')
        extraOptions.grid(row=2, column=1, sticky=N+S+E+W)
	
        l = Label(extraOptions, text='Wavelets')
        l.pack(side=TOP, fill=X, pady=(5,0), padx=5)

        dic = {'Mexican Hat':['MexicanHat'], 'Morlet':['Morlet','MorletReal'], 'Haar':['Haar','HaarW']}#, 'Daubechies':'db', 'Symlets':'sym', 'Coiflets':'coif', 
            #'Biorthogonal':'bior', 'Reverse Biorthogonal':'rbio', 'Discrete Meyer':'dmey'}
        self.dic=dic
        self.family = StringVar()
        self.family.set('Mexican Hat')#'Daubechies')
        self.wavelet = StringVar()
        self.wavelet.set('MexicanHat')#'db4')

        #if self.family.get() == 'Mexican Hat' or self.family.get() == 'Morlet':
        wavelets = [self.dic[self.family.get()]]
        #else:
        #    wavelets = pywt.wavelist(self.dic[self.family.get()])
        
        familyMenu = OptionMenu(extraOptions, self.family, *dic.keys(), command=self.updateFamily)
        familyMenu.pack(side=TOP, fill=X,pady=(0,0),padx=5)
        waveletMenu = OptionMenu(extraOptions,self.wavelet, *wavelets, command=(lambda x : self.updatePlots()))
        waveletMenu.pack(side=TOP, fill=X, pady=(0,5),padx=5)
        
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
        #if self.family.get() == 'Mexican Hat' or self.family.get() == 'Morlet':
        wavelets = self.dic[self.family.get()]
        #else:
        #   wavelets = pywt.wavelist(self.dic[self.family.get()])
        
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

        '''
        if self.family.get() == 'Mexican Hat' or self.family.get() == 'Morlet':
            wave = eval(self.wavelet.get())
        else:
            wave = (lambda x,y: other(x,y,self.wavelet.get()))
        '''
        wave = eval(self.wavelet.get())
        
        if (name,wave) not in self.cwt.keys(): self.cwt[(name,wave)] = wave(data, 1).getdata()
        elif self.cwt[(name,wave)].shape[1] < M: self.cwt[(name,wave)] = wave(data, 1).getdata()
        '''
        elif len(self.cwt[(name,wave)]) < self.maxScale.get(): 

            new = signal.cwt(data, wave, arange(len(self.cwt[(name,wave)])+1, self.maxScale.get()+1))
            self.cwt[(name,wave)] = np.append(self.cwt[(name,wave)], new, axis=0)
        '''
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
            
            color = self.contourColor.get()
            #print color
            color = None if color == 0 else 'k'
            #print color
            cs = axes[1].contour(plotcwt, colors=color)
            axes[1].clabel(cs, inline=1)
            
        else:
            axes[1] = figs[1].add_subplot(111, projection='3d')


            shape = plotcwt.shape
            #print shape, .shape
            shape = (shape[0], M)
            plotcwt = plotcwt[:,:M]
            Y = np.array([range(shape[0]) for i in range(shape[1])]).T
            X = np.array([[i]*shape[0] for i in range(shape[1])]).T

            self.plot3D = axes[1].plot_surface(X ,Y,plotcwt,cmap=matplotlib.cm.jet, linewidth=0)

        
        lines[0].set_data(t,data)
        axes[0].axis([0,len(data),min(data),max(data)])
        axes[1].axis([0,len(data),0,self.maxScale.get()])
        
        self.formatAxes(axes[0],t,data,'Time (sec)','Amplitude',self.filename.get())
        self.formatAxes(axes[1],t,range(self.maxScale.get()),'Time (sec)','Scale','Scalogram of '+self.filename.get())
        
        self.sliders[0][1].config(to=len(data)/2)
        
        for axis in axes:
            axis.get_figure().canvas.draw_idle()
  
if __name__ == "__main__":
    root = Tk()
    WaveletWindow(root)
    root.mainloop()    
