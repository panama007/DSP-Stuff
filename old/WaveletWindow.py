from FourierWindow import *
from wavelets2 import *


class WaveletWindow(FourierWindow):
        
    def __init__(self, root):
        self.title = 'Wavelet Analysis'
    
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
        extraOptions.grid(row=2, column=1, sticky=N+S+E+W, pady=self.pads[1], padx=self.pads[0])
	
        l = Label(extraOptions, text='Wavelets')
        l.pack(side=TOP, fill=X, pady=(self.pads[1],0), padx=self.pads[0])

        dic = {'Mexican Hat':['MexicanHat'], 'Morlet':['MorletReal','Morlet'], 'Haar':['Haar','HaarW']}#, 'Daubechies':'db', 'Symlets':'sym', 'Coiflets':'coif', 

        self.dic=dic
        self.family = StringVar()
        self.family.set('Mexican Hat')#'Daubechies')
        self.wavelet = StringVar()
        self.wavelet.set('MexicanHat')#'db4')

        wavelets = [self.dic[self.family.get()]]
        
        familyMenu = OptionMenu(extraOptions, self.family, *dic.keys(), command=self.updateFamily)
        familyMenu.pack(side=TOP, fill=X,pady=0,padx=self.pads[0])
        waveletMenu = OptionMenu(extraOptions,self.wavelet, *wavelets, command=(lambda x : self.updatePlots()))
        waveletMenu.pack(side=TOP, fill=X, pady=(0,self.pads[1]),padx=self.pads[0])
        
        self.waveletMenu=waveletMenu
        
        
        tableFrame = Frame(self.leftPane, bg='grey')
        tableFrame.grid(row=3,column=1,sticky=N+S+E+W)
        
        headings = [("Frequency Peaks", ["Peak", "Frequency", "Amplitude"])]
        frames = [tableFrame]
        heights = [20]
        
        [self.peaksTable] = self.makeTables(headings, frames, heights)
    	
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        varNames = ['Max Scale']
        varLimits = [(1,512)]
        varRes = [2]
        varDTypes = [IntVar]
        varDefaults = [128]
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane((2,2), varValues)
        
        self.maxScale = self.vars[0]
        
    
    def updateFamily(self,_):
        self.waveletMenu['menu'].delete(0,'end')
        def c(val):
            self.wavelet.set(val)

            self.updatePlots()

        wavelets = self.dic[self.family.get()]

        for wavelet in wavelets:

            self.waveletMenu['menu'].add_command(label=wavelet,command=lambda wavelet=wavelet:c(wavelet))

        self.wavelet.set(wavelets[0])
        self.updatePlots()
    
  
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):
        self._initSignals(numMarkers=1)
        
        self.figs[1].canvas.mpl_connect('button_press_event', self.mouseCallback)
        self.slope = [None]*4
        
        self.signalFromFile()

    def mouseCallback(self, event):    
        if not event.ydata: return
        
        s = self.axes[1].format_coord(event.xdata,event.ydata)
        
        yind1 = s.find('y')
        xind1 = s.find('x')
        yind2 = yind1 + s[yind1:].find(' ')
        xind2 = xind1 + s[xind1:].find(' ')
        y = int(float(s[yind1+2:yind2]))
        x = int(float(s[xind1+2:xind2]))
        
        data = self.signal
        N = len(data)
        name = self.filename.get()
        wave = eval(self.wavelet.get())
        cwt = self.cwt[(name,wave,N)]
        
        if event.button == 1:
            scale = y
            if scale < 0: scale = 0

            t = arange(N)
            delta_w = 1./(N-1)
            w = np.linspace(0, delta_w*(N/2-1), N/2)
            
            subsignal = cwt[scale]
            F = np.abs(np.fft.fft(subsignal))[:N/2]
            
            self.updatePeakTable(w,F,0,self.peaksTable,3)
            
            self.lines[2].set_data(t,subsignal)
            self.lines[3].set_data(w,F)
            
            self.formatAxes(self.axes[2],t,subsignal,'Time (sec)','Amplitude','Subsignal at Scale %i'%scale)
            self.formatAxes(self.axes[3],w,F,'Frequency (Hz)', 'Magnitude', 'FFT of Subsignal')
            
            self.axes[2].get_figure().canvas.draw_idle()
            self.axes[3].get_figure().canvas.draw_idle()
            
        elif event.button == 3:
            if (bool(self.slope[0]) == bool(self.slope[1])) or (name, wave, N) != self.slope[2]: 
                self.slope[0] = (x,y)
                self.slope[1] = None
                self.slope[2] = (name, wave, N)
                if self.slope[3]: self.slope[3].pop(0).remove()
                
            elif self.slope[0] and not self.slope[1]:
                self.slope[1] = (x,y)
                
                xs = [self.slope[0][0], self.slope[1][0]]
                ys = [self.slope[0][1], self.slope[1][1]]
                m = (np.abs(cwt[ys[1]][xs[1]]) - np.abs(cwt[ys[0]][xs[0]])) / np.sqrt((ys[0]-ys[1])**2+(xs[0]-xs[1])**2)
                
                self.slope[3] = self.axes[1].plot(xs, ys, label='Avg. Slope = %f'%m, color='k', linewidth=2)
                self.axes[1].legend()
                self.axes[1].get_figure().canvas.draw_idle()
                
            

    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    
    def updatePlots(self):
        data = self.signal
        N = len(data)
        t = arange(N)
        name = self.filename.get()

        wave = eval(self.wavelet.get())
        
        if (name,wave,N) not in self.cwt.keys(): self.cwt[(name,wave,N)] = wave(data, 1).getdata()

        self.signalChanged = False
        
        axes = self.axes       
        figs = self.figs
        lines = self.lines
                
        plotcwt = abs(self.cwt[(name,wave,N)][:self.maxScale.get()])

        figs[1].clf()
        if self.plotType.get() == 0:
            axes[1] = figs[1].add_subplot(111)
            
            axes[1].imshow(plotcwt,aspect='auto')
        elif self.plotType.get() == 2:
            axes[1] = figs[1].add_subplot(111)
            
            color = self.contourColor.get()
            color = None if color == 0 else 'k'
            cs = axes[1].contour(plotcwt, colors=color)
            axes[1].clabel(cs, inline=1)
            
        else:
            axes[1] = figs[1].add_subplot(111, projection='3d')

            shape = plotcwt.shape
            Y = np.array([range(shape[0]) for i in range(shape[1])]).T
            X = np.array([[i]*shape[0] for i in range(shape[1])]).T

            self.plot3D = axes[1].plot_surface(X ,Y,plotcwt,cmap=matplotlib.cm.jet, linewidth=0)

        
        lines[0].set_data(t,data)
        axes[0].axis([0,len(data),min(data),max(data)])
        axes[1].axis([0,len(data),0,self.maxScale.get()])
        
        self.formatAxes(axes[0],t,data,'Time (sec)','Amplitude',self.filename.get())
        self.formatAxes(axes[1],t,range(self.maxScale.get()),'Time (sec)','Scale','Scalogram of '+self.filename.get() +'   (LClick to select subsignal, RClick twice for slope)', True)
        
        self.sliders[0][1].config(to=len(data)/2-2)
        
        for fig in self.figs:
            fig.canvas.draw_idle()
            #fig.subplots_adjust(bottom = 0.18)
  
if __name__ == "__main__":
    root = Tk()
    WaveletWindow(root)
    
    if os.name == "nt": root.wm_state('zoomed')
    else: root.attributes('-zoomed', True)

    root.mainloop()    
