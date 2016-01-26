from FourierWindow import *


class MRAWindow(FourierWindow):
        
    def __init__(self, root):
        self.title = 'MRA Decomposition'
    
        self.numLevels=10
        self.signalChanged=True
        
        self.signalType = 0
    
        FourierWindow.__init__(self, root)
  
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        levelTexts = ['Level %i'%i for i in range(-1,20)]
        levelVals = range(-1,20)
        
        wavelets = pywt.wavelist()
    
        varTitles = ['Mode','Frequency / PPM']#, 'Levels']
        varDTypes = [StringVar, IntVar]#, IntVar]
        varDefaults = ['Decomposition', 0]#, -1]
        varTexts = [['Decomposition','Cumulative Reconstruction', 'Arbitrary Reconstruction'],['Frequency', 'PPM']]#, levelTexts]
        varVals = [['Decomposition','Cumulative Reconstruction', 'Arbitrary Reconstruction'], range(3)]#, levelVals]
        # , 'Arbitrary Reconstruction'
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        self._makeLeftPane(optionsSpecs, True)
        
        self.mode = self.options[0]
        self.freq = self.options[1]
        #self.level = self.options[2]

        extraOptions = Frame(self.leftPane, bg='grey')
        extraOptions.grid(row=2, column=1, sticky=N+S+E+W)
        tableFrame1 = Frame(self.leftPane, bg='grey')
        tableFrame1.grid(row=1,column=2,sticky=N+S+E+W, pady=self.pads[1], padx=self.pads[0])
        tableFrame2 = Frame(self.leftPane, bg='grey')
        tableFrame2.grid(row=2,column=2,sticky=N+S+E+W, pady=self.pads[1], padx=self.pads[0])

        titlePane = Frame(extraOptions)
        titlePane.pack(fill=X, pady=(self.pads[1],0), padx=self.pads[0])
        # Wavelets Select
        Label(titlePane, text='Wavelets').pack(fill=BOTH, side=LEFT, expand=1)
        Button(titlePane, text='?', command=self.popupWavelet).pack(fill=BOTH, side=LEFT)

        dic = {'Haar':'haar', 'Daubechies':'db', 'Symlets':'sym', 'Coiflets':'coif', 
            'Biorthogonal':'bior', 'Reverse Biorthogonal':'rbio', 'Discrete Meyer':'dmey'}
        self.dic=dic
        self.family = StringVar()
        self.family.set('Haar')
        self.wavelet = StringVar()
        self.wavelet.set('haar')

        familyMenu = OptionMenu(extraOptions, self.family, *dic.keys(), command=self.updateFamily)
        familyMenu.pack(fill=BOTH,pady=0,padx=self.pads[0])
        waveletMenu = OptionMenu(extraOptions,self.wavelet, *pywt.wavelist(dic[self.family.get()]), command=(lambda x : self.updatePlots()))
        waveletMenu.pack(fill=BOTH, pady=(0,self.pads[1]),padx=self.pads[0])
        
        self.waveletMenu=waveletMenu
        ############################
        self.radioButtons.append([])
        self.options.append(IntVar())
        self.options[-1].set(-1)
    
        l = Label(extraOptions, text='Levels')
        l.pack(fill=X, pady=(self.pads[1],0), padx=self.pads[0])

        frame = Frame(extraOptions)
        frame.pack(fill=BOTH,pady=(0,self.pads[1]),padx=self.pads[0])

        levelTexts = ['Level %i'%i for i in range(-1,20)]
        self.max = 20
        self.levels = [IntVar() for i in levelTexts]
        self.oldlevels = [0]*len(self.levels)
        
        for j in range(len(levelTexts)):
            cb = Checkbutton(frame, text=levelTexts[j], variable=self.levels[j], command=self.selectLevel)
            cb.grid(row=j+1,sticky=W,padx=(self.pads[0],0))
            
            self.radioButtons[-1].append(cb)
                        
        self.level = self.options[2]
        
        headings = [("Energy Table (Normalized)", ["Level", "Energy in T", "Energy in F", "% Total Energy"]), 
                    ("Frequencyand PPM Peaks", ["Peak", "Frequency", "PPM", "Amplitude"])]
        frames = [tableFrame1, tableFrame2]
        heights = [len(levelVals)+1, 10]
        
        [self.energyTable, self.peaksTable] = self.makeTables(headings, frames, heights)
     
    def selectLevel(self):
        levels = [self.levels[i] for i in range(self.max + 1)]
        levelvals = [l.get() for l in levels]
        
        dif = np.array(self.oldlevels[:self.max+1]) - np.array(levelvals)
        m = np.nonzero(dif)[0][0]
        
        if self.mode.get() == 'Cumulative Reconstruction': 
            for i in range(len(levels)):
                if i <= m:
                    levels[i].set(1)
                else:
                    levels[i].set(0)
            self.level.set(m-1)
        
        elif self.mode.get() == 'Decomposition': 
            for i in range(len(levels)):
                if i == m:
                    levels[i].set(1)
                else:
                    levels[i].set(0)
            self.level.set(m-1)
        
        
        self.oldlevels = [l.get() for l in self.levels]
        #if self.mode.get() == 'Decomposition':
            
        
        self.updatePlots()
     
    def popupWavelet(self):
        popup = Toplevel()
        fig = Figure(figsize=(5,5))
        ax0 = fig.add_subplot(211)
        ax1 = fig.add_subplot(212)

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.show()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        
        wave = self.convertDaub(self.wavelet.get(),1)
        w = pywt.Wavelet(wave)
        f = w.wavefun()
        ax0.plot(f[0])
        ax0.plot(f[1])
        if os.name == 'nt':
            ax0.legend(['Father Wavelet', 'Mother Wavelet'], fontsize=10)
        else:
            ax0.legend(['Father Wavelet', 'Mother Wavelet'])
        ax0.axis([0,len(f[0]),min(min(f[0]),min(f[1]))-0.1,max(max(f[0]),max(f[1]))+0.1])
        
        n = w.dec_len
        F = abs(np.fft.fft(w.dec_lo)[:n/2+1])**2/2
        F2 = abs(np.fft.fft(w.dec_hi)[:n/2+1])**2/2
        ax1.plot(F)
        ax1.plot(F2)
        if os.name == 'nt':
            ax1.legend(['Low Pass Filter', 'High Pass Filter'], loc=7, fontsize=10)
        else:
            ax1.legend(['Low Pass Filter', 'High Pass Filter'], loc=7)
        ax1.axis([0,len(F)-1,min(min(F),min(F2))-0.1,max(max(F),max(F2))+0.1])
        
        fig.tight_layout()
        
    def convertDaub(self, name,dir=0):
        if name[:2] == 'db':
            n = int(name[2:])*2 if dir == 0 else int(name[2:])/2
            return 'db'+str(n)
        return name
    
    def mouseCallback1(self, event):
        s = self.axes[3].format_coord(event.xdata,event.ydata)
        
        yind1 = s.find('y')
        yind2 = yind1 + s[yind1:].find(' ')
        y = float(s[yind1+2:yind2])
        
        [w,F] = self.Fplot
        
        
        if event.button == 1:
            if self.threshold[0][1]: self.threshold[0][1].pop(0).remove()
            
            self.threshold[0][0] = y
            self.threshold[0][1] = self.axes[3].plot(w,[y]*len(w), color='k', linewidth=2)
            
        elif event.button == 3:
            if self.threshold[0][1]: self.threshold[0][1].pop(0).remove()
            
            self.threshold[0][0] = None
            
        [f,w,w2,m] = self.params    
        self.updatePeakTable(w,F,0,0,self.peaksTable,3,ppmTable=1,ppmPlot=self.freq.get())
        self.axes[3].get_figure().canvas.draw_idle()
     
    def mouseCallback2(self, event):
        s = self.axes[0].format_coord(event.xdata,event.ydata)
        
        xind1 = s.find('x')
        xind2 = xind1 + s[xind1:].find(' ')
        x = float(s[xind1+2:xind2])
        
        [f,w,w2,m] = self.params
        
        if event.button == 1:
            if (bool(self.selector[0]) == bool(self.selector[1])) or self.filename.get() != self.selector[2]: 
                self.selector[0] = x
                self.selector[1] = None
                self.selector[2] = self.filename.get()
                for line in self.selector[3]: 
                    if line: line.remove()
                self.selector[3][0] = self.axes[0].axvline(x, color='r')
                
            elif self.selector[0] and not self.selector[1]:
                self.selector[1] = x
                if self.selector[1] < self.selector[0]:
                    tmp = self.selector[0]
                    self.selector[0] = self.selector[1]
                    self.selector[1] = tmp
                
                t = arange(len(f))
                indmin, indmax = np.searchsorted(t, (self.selector[0], self.selector[1]))
                indmax = min(len(t) - 1, indmax)
                
                subf = f[indmin:indmax]
                s = np.sign(subf)
                s[s==0] = -1
                crossings = np.where(np.diff(s))[0]
                
                energy = sum(subf * np.conjugate(subf))
                
                loc = [min(t) + (max(t)-min(t))*0.6, min(f) + (max(f)-min(f))*0.9]
                self.selector[3][2] = self.axes[0].text(loc[0],loc[1],'t1: %i ms   t2: %i ms\n# of Zero-Crossings: %i\nEnergy: %0.05f'%(t[indmin],t[indmax],len(crossings),energy),bbox={'facecolor':'white','alpha':1,'pad':10})
                
                self.selector[3][1] = self.axes[0].axvline(x, color='r')
                #self.axes[1].legend()
        #elif event.button == 3:
        #    if self.threshold[0][1]: self.threshold[0][1].pop(0).remove()
        #    
        #    self.threshold[0][0] = None
            
        
        self.axes[0].get_figure().canvas.draw_idle()
     
    def mouseCallback(self, event):   
        #print event.ydata
        if (bool(event.ydata) & (event.inaxes == self.axes[3])):
            self.mouseCallback1(event)
        elif (bool(event.ydata) & (event.inaxes == self.axes[0])):
            self.mouseCallback2(event)
    
    def updateFamily(self,_):
        self.waveletMenu['menu'].delete(0,'end')
        def c(val):
            self.wavelet.set(val)
            #print val
            self.updatePlots()

        for wavelet in pywt.wavelist(self.dic[self.family.get()]):
            wavelet = self.convertDaub(wavelet)
            self.waveletMenu['menu'].add_command(label=wavelet,command=lambda wavelet=wavelet:c(wavelet))

        default = self.convertDaub(pywt.wavelist(self.dic[self.family.get()])[0])
        self.wavelet.set(default)
        self.updatePlots()
    
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        '''varNames = ['Omega0']
        varLimits = [(1,100)]
        varRes = [0.1]
        varDTypes = [DoubleVar]
        varDefaults = [5]
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]'''
        
        self._makeRightPane((2,2))#, [varValues])
        
        #self.omega = self.vars[0][0]
        
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):
        self._initSignals(numMarkers=1)
        
        self.fig.canvas.mpl_connect('button_press_event', self.mouseCallback)
        self.threshold = [[None]*2]
        self.selector = [None,None,None,[None,None,None]]

        self.signalFromFile()
    
    def updateParams(self):    
        f = self.signal
        wave = self.convertDaub(self.wavelet.get(),1)
        m = pywt.wavedec(f,wave, mode='per')
        s = pywt.waverec(m,wave, mode='per')
        
        N = len(s)
        delta_w = 1./(N-1)
        w = np.linspace(0, delta_w*(N/2-1), num=N/2)
        
        N2 = len(f)
        delta_w = 1./(N2-1)
        w2 = np.linspace(0, delta_w*(N2/2-1), num=N2/2)
        
        self.params = [f,w,w2,m]

    def updateLevels(self):
        l = self.level.get()
        wave = self.convertDaub(self.wavelet.get(),1)
        max = pywt.dwt_max_level(len(self.signal),pywt.Wavelet(wave))
        self.max = max
        
        if l > max:
            self.level.set(max-1)
            
        #mode = self.mode.get()
        for i in range(21):
            if i <= max:
                self.radioButtons[2][i].grid()
            else:
                self.radioButtons[2][i].grid_remove()
        
    def updateEnergyTable(self): #TODO, clean this up
        wave = self.convertDaub(self.wavelet.get(),1)
        max = pywt.dwt_max_level(len(self.signal),pywt.Wavelet(wave))
        [f,w,w2,m] = self.params

        
        for i in range(22):
            row = self.energyTable[i]
            
            if i <= max+1:
                subm = list(m)
                if i != max+1:  
                    for j in range(max):
                        if j != i:
                            subm[j] = [0]*len(m[j])
                
                wave = self.convertDaub(self.wavelet.get(),1)
                subsignal = pywt.waverec(subm,wave, mode='per')
                F = np.fft.fft(subsignal)[:len(subsignal)/2]
                
                for j in range(4):
                    row[j][0].grid()
                    if j == 0:
                        if i == max+1:
                            row[j][1].set('Total')
                        else:
                            row[j][1].set('Levels %i'%(i-1))
                    elif j == 1:
                        row[j][1].set('%f'%sum(subsignal**2))
                    elif j == 2:
                        row[j][1].set('%f'%(sum(F*np.conjugate(F))/len(F)))
                    else:
                        percent = (100*sum(subsignal*np.conjugate(subsignal))/sum(f*np.conjugate(f))).real
                        row[j][1].set('%f %%'%percent)
            else:
                for j in range(4):
                    row[j][0].grid_remove()
                    
                
    
    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    #TODO keep variable of FFT of each level so don't have to compute each time
    def updatePlots(self):

        #if self.signalChanged: 
        self.updateParams()
        self.updateLevels()
        self.updateEnergyTable()
        #self.signalChanged = False
        
        [f,w,w2,m] = self.params
        #print m[self.level.get()+1]
        
        #print "hi"
        
        levelsText = 'Level(s) '
        for i in range(self.max+1):
            if self.levels[i].get() == 1:
                levelsText += '%i+'%(i-1)
            else:
                m[i] = [0]*len(m[i])
        levelsText = levelsText[:-1]
        '''    
        if self.mode.get() == 'Cumulative Reconstruction':
            #levelsText = "Level(s) -1"+''.join(map(lambda i: '+%i'%i, range(self.level.get()+1)))
            for i in range(self.level.get()+2,len(m)):
                m[i] = [0]*len(m[i])
        else:
            #levelsText = "Level %i"%(self.level.get())
            for i in range(len(m)):
                if i != self.level.get()+1:
                    m[i] = [0]*len(m[i])
        '''
        wave = self.convertDaub(self.wavelet.get(),1)
        s = pywt.waverec(m,wave, mode='per')
        
        N = len(f)
        t = arange(N)
        
        N2 = len(f)
        F2 = fft.fft(f)
        F2 = abs(F2[:N2/2])
        
        F = fft.fft(s)
        F = abs(F[:len(s)/2])
        
        #print sum(F2*np.conjugate(F2))/len(F2)
        #print sum(F*np.conjugate(F))/len(F)
        
        lines = self.lines
        axes = self.axes
        
        #print t.shape, f.shape
        lines[0].set_data(t,f)
        axes[1].cla()
        axes[1].grid()
        #print w2.shape, F2.shape
        lines[1], = axes[1].plot(w2,F2)
        self.formatAxes(axes[0],t,f,'Time (ms)','Amplitude',self.filename.get())
        self.formatAxes(axes[1],w2,F2,'Frequency (kHz)','Amplitude','FFT of '+self.filename.get())
        #print "hi"
        mean = sum([amp*freq for (freq, amp) in zip(w, F2)])/sum(F2)
        midpoint = sum(F2)/2.
        median = 0
        cur = 0
        for ind in range(len(w)):
            cur += F2[ind]
            if cur >= midpoint:
                median = w[ind]
                break
        stddev = (sum([(freq-mean)**2*amp for (freq,amp) in zip(w, F2)])/sum(F2))**0.5
        
        
        loc = [min(w) + (max(w)-min(w))*0.7, min(F2) + (max(F2)-min(F2))*0.9]
        axes[1].text(loc[0],loc[1],'Mean: %0.5f\nMedian: %0.05f\nStd. Dev: %0.05f'%(mean,median,stddev),bbox={'facecolor':'white','alpha':1,'pad':10})
        
        axisLabel = 'Frequency (kHz)'
        self.updatePeakTable(w,F,0,0,self.peaksTable,3,ppmTable=1,ppmPlot=self.freq.get()) 
        if self.freq.get() == 1:
            w = self.freq2ppm(w)
            axisLabel = 'PPM'
        
        
        
        

        lines[2].set_data(arange(len(s)),s)
        self.Fplot = [w,F]
        axes[3].cla()
        axes[3].grid()
        lines[3], = axes[3].plot(w,F)
        
        mean = sum([amp*freq for (freq, amp) in zip(w, F)])/sum(F)
        midpoint = sum(F)/2.
        cur = 0
        for ind in range(len(w)):
            cur += F[ind]
            if cur >= midpoint:
                median = w[ind]
                break
        stddev = (sum([(freq-mean)**2*amp for (freq,amp) in zip(w, F)])/sum(F))**0.5     
               
        
        self.formatAxes(axes[2],t,s,'Time (ms)','Amplitude',levelsText)
        self.formatAxes(axes[3],w,F,axisLabel,'Amplitude','FFT of '+levelsText)
        if self.freq.get() == 1:
            axes[3].set_xlim([max(w),0])
        xlim, ylim = axes[3].get_xlim(), axes[3].get_ylim()
        loc = [xlim[0] + (xlim[1]-xlim[0])*0.7, ylim[0] + (ylim[1]-ylim[0])*0.8]
        axes[3].text(loc[0],loc[1],'Mean: %0.5f\nMedian: %0.05f\nStd. Dev: %0.05f'%(mean,median,stddev),bbox={'facecolor':'white','alpha':1,'pad':10})
        
        [ax.axhline(color='k') for ax in self.axes]
        #for fig in self.figs:
        self.fig.canvas.draw_idle()
            #fig.tight_layout()
        
if __name__ == "__main__":
    root = Tk()
    
    note = Notebook(root) 
    tab = Frame(note)
    obj = MRAWindow(tab)
    note.add(tab, text=obj.title)

    note.pack(fill=BOTH, expand=1)
    
    if os.name == "nt": root.wm_state('zoomed')
    else: root.attributes('-zoomed', True)

    root.mainloop()  
