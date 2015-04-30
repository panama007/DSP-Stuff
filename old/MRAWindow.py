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
    
        varTitles = ['Mode','Frequency or PPM', 'Levels']
        varDTypes = [StringVar, IntVar, IntVar]
        varDefaults = ['Decomposition', 0, -1]
        varTexts = [['Decomposition','Cumulative Reconstruction'],['Frequency', 'PPM'], levelTexts]
        varVals = [['Decomposition','Cumulative Reconstruction'], range(2), levelVals]
        # , 'Arbitrary Reconstruction'
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        self._makeLeftPane(optionsSpecs, True)
        
        self.mode = self.options[0]
        self.freq = self.options[1]
        self.level = self.options[2]

        extraOptions = Frame(self.leftPane, bg='grey')
        extraOptions.grid(row=2, column=1, sticky=N+S+E+W)
        tableFrame1 = Frame(self.leftPane, bg='grey')
        tableFrame1.grid(row=1,column=2,sticky=N+S+E+W, pady=self.pads[1], padx=self.pads[0])
        tableFrame2 = Frame(self.leftPane, bg='grey')
        tableFrame2.grid(row=2,column=2,sticky=N+S+E+W, pady=self.pads[1], padx=self.pads[0])

        titlePane = Frame(extraOptions)
        titlePane.pack(fill=X, pady=(self.pads[1],0), padx=self.pads[0])
        
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
        
        headings = [("Energy Table", ["Level", "Energy in T", "Energy in F", "% Total Energy"]), 
                    ("Frequency Peaks", ["Peak", "Frequency", "Amplitude"])]
        frames = [tableFrame1, tableFrame2]
        heights = [len(levelVals)+1, 10]
        
        [self.energyTable, self.peaksTable] = self.makeTables(headings, frames, heights)
        '''
        table = Frame(tableFrame1)
        table.pack(fill=BOTH, pady=5, padx=5)
        Label(table, text="Energy Table").grid(row=0,column=0,columnspan=4)
        Label(table, text="Level").grid(row=1,column=0)
        Label(table, text="Energy in T").grid(row=1,column=1)
        Label(table, text="Energy in F").grid(row=1,column=2)
        Label(table, text="% of Total Energy").grid(row=1,column=3)
        
        self.table = []
        for i in range():
            row = []
            for j in range(4):
                tv = StringVar()
                l = Label(table, textvariable=tv)
                l.grid(row=i+2,column=j)
                row.append([l,tv])
            self.table.append(row)
            
        
        table2 = Frame(tableFrame2)
        table2.pack(fill=BOTH, pady=5, padx=5)
        [table2.columnconfigure(i,weight=1) for i in range(3)]
        Label(table2, text="Frequency Peaks").grid(row=0,column=0,columnspan=3)
        Label(table2, text="Peak").grid(row=1,column=0)
        Label(table2, text="Frequency").grid(row=1,column=1)
        Label(table2, text="Amplitude").grid(row=1,column=2)
        
        self.table2 = []
        for i in range(10):
            row = []
            for j in range(3):
                tv = StringVar()
                l = Label(table2, textvariable=tv)
                l.grid(row=i+2,column=j,sticky=N+S+E+W)
                row.append([l,tv])
            self.table2.append(row)
        '''
        
    def popupWavelet(self):
        popup = Toplevel()
        fig = Figure(figsize=(5,5))
        ax0 = fig.add_subplot(211)
        ax1 = fig.add_subplot(212)

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.show()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        
        w = pywt.Wavelet(self.wavelet.get())
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
    
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        self._makeRightPane((2,2))
        
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):
        self._initSignals(numMarkers=1)

        self.signalFromFile()
        
    def updateParams(self):    
        f = self.signal

        m = pywt.wavedec(f,self.wavelet.get(), mode='per')
        
        N = len(f)
        delta_w = 1./(N-1)
        w = np.linspace(0, delta_w*(N/2-1), num=N/2)
        
        self.params = [f,w,m]

    def updateLevels(self):
        l = self.level.get()
        max = pywt.dwt_max_level(len(self.signal),pywt.Wavelet(self.wavelet.get()))
        
        if l > max:
            self.level.set(max-1)
            
        #mode = self.mode.get()
        for i in range(21):
            if i <= max:
                self.radioButtons[2][i].grid()
            else:
                self.radioButtons[2][i].grid_remove()
        
    def updateEnergyTable(self): #TODO, clean this up
        max = pywt.dwt_max_level(len(self.signal),pywt.Wavelet(self.wavelet.get()))
        [f,w,m] = self.params

        
        for i in range(22):
            row = self.energyTable[i]
            
            if i <= max+1:
                subm = list(m)
                if i != max+1:  
                    for j in range(max):
                        if j != i:
                            subm[j] = [0]*len(m[j])
                subsignal = pywt.waverec(subm,self.wavelet.get(), mode='per')
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
        
        [f,w,m] = self.params
        #print m[self.level.get()+1]
        
        if self.freq.get() == 1:
            w = 4.7-2*pi/63.8664*w
        
        if self.mode.get() == 'Cumulative Reconstruction':
            levelsText = "Level(s) -1"+''.join(map(lambda i: '+%i'%i, range(self.level.get()+1)))
            for i in range(self.level.get()+2,len(m)):
                m[i] = [0]*len(m[i])
        else:
            levelsText = "Level %i"%(self.level.get())
            for i in range(len(m)):
                if i != self.level.get()+1:
                    m[i] = [0]*len(m[i])
        #print m
        s = pywt.waverec(m,self.wavelet.get(), mode='per')
        
        N = len(s)
        t = arange(N)
        F = fft.fft(s)
        F = abs(F[:N/2])
        
        F2 = fft.fft(f)
        F2 = abs(F2[:N/2])
        
        #print sum(F2*np.conjugate(F2))/len(F2)
        #print sum(F*np.conjugate(F))/len(F)
        
        lines = self.lines
        axes = self.axes
        
        lines[0].set_data(t,f)
        lines[1].set_data(w,F2)
        
        lines[2].set_data(t,s)
        lines[3].set_data(w,F)
        
        self.updatePeakTable(w,F,0,self.peaksTable,3)
        
        axisLabel = 'Frequency (Hz)' if self.freq.get() == 0 else 'PPM'
        
        self.formatAxes(axes[0],t,f,'Time (sec)','Amplitude',self.filename.get())
        self.formatAxes(axes[1],w,F2,axisLabel,'Amplitude','FFT of '+self.filename.get())
        self.formatAxes(axes[2],t,s,'Time (sec)','Amplitude',levelsText)
        self.formatAxes(axes[3],w,F,axisLabel,'Amplitude','FFT of '+levelsText)
        
        for fig in self.figs:
            fig.canvas.draw_idle()
            #fig.tight_layout()
        
if __name__ == "__main__":
    root = Tk()
    MRAWindow(root)
    
    if os.name == "nt": root.wm_state('zoomed')
    else: root.attributes('-zoomed', True)

    root.mainloop()  
    
