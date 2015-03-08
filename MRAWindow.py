from FourierWindow import *


class MRAWindow(FourierWindow):
        
    def __init__(self, root):
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
    
        varTitles = ['Mode', 'Levels']
        varDTypes = [StringVar, IntVar]
        varDefaults = ['Cumulative Reconstruction', -1]
        varTexts = [['Cumulative Reconstruction', 'Decomposition'], levelTexts]
        varVals = [['Cumulative Reconstruction', 'Decomposition'], levelVals]
        # , 'Arbitrary Reconstruction'
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        self._makeLeftPane(optionsSpecs, True)
        
        self.mode = self.options[0]
        self.level = self.options[1]


        l = Label(self.leftPane, text='Wavelets')
        l.pack(fill=X, pady=(15,0), padx=5)

        dic = {'Haar':'haar', 'Daubechies':'db', 'Symlets':'sym', 'Coiflets':'coif', 
            'Biorthogonal':'bior', 'Reverse Biorthogonal':'rbio', 'Discrete Meyer':'dmey'}
        self.dic=dic
        self.family = StringVar()
        self.family.set('Haar')
        self.wavelet = StringVar()
        self.wavelet.set('haar')

        familyMenu = OptionMenu(self.leftPane, self.family, *dic.keys(), command=self.updateFamily)
        familyMenu.pack(fill=BOTH,pady=(0,0),padx=5)
        waveletMenu = OptionMenu(self.leftPane,self.wavelet, *pywt.wavelist(dic[self.family.get()]), command=(lambda x : self.updatePlots()))
        waveletMenu.pack(fill=BOTH, pady=(0,15),padx=5)
        
        self.waveletMenu=waveletMenu
        
        table = Frame(self.leftPane)
        table.pack(fill=BOTH, pady=15, padx=5)
        Label(table, text="Energy Table").grid(row=0,column=0,columnspan=3)
        Label(table, text="Level").grid(row=1,column=0)
        Label(table, text="Energy").grid(row=1,column=1)
        Label(table, text="% of Total Energy").grid(row=1,column=2)
        
        self.table = []
        for i in range(len(levelVals)+1):
            row = []
            for j in range(3):
                tv = StringVar()
                l = Label(table, textvariable=tv)
                l.grid(row=i+2,column=j)
                row.append([l,tv])
            self.table.append(row)     
    
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
        axes = self.axes
        lines = []
        dummy = [0]
        for axis in axes:
            l,=axis.plot(dummy)
            lines.append(l)

        self.lines = lines

        self.signalFromFile()
        
    def updateParams(self):    
        f = self.signal

        m = pywt.wavedec(f,self.wavelet.get())
        
        N = len(f)
        delta_w = 2*pi/(N-1)
        w = linspace(0, delta_w*(N/2-1), num=N/2)
        
        self.params = [f,w,m]

    def updateLevels(self):
        l = self.level.get()
        max = pywt.dwt_max_level(len(self.signal),pywt.Wavelet(self.wavelet.get()))
        
        if l > max:
            self.level.set(max-1)
            
        #mode = self.mode.get()
        for i in range(21):
            if i <= max:
                self.radioButtons[1][i].grid()
            else:
                self.radioButtons[1][i].grid_remove()
        
    def updateEnergyTable(self): #TODO, clean this up
        max = pywt.dwt_max_level(len(self.signal),pywt.Wavelet(self.wavelet.get()))
        [f,w,m] = self.params

        
        for i in range(22):
            row = self.table[i]
            
            if i <= max+1:
                subm = list(m)
                if i != max+1:  
                    for j in range(max):
                        if j != i:
                            subm[j] = [0]*len(m[j])
                subsignal = pywt.waverec(subm,self.wavelet.get())
                
                
                for j in range(3):
                    row[j][0].grid()
                    if j == 0:
                        if i == max+1:
                            row[j][1].set('Total')
                        else:
                            row[j][1].set('Levels %i'%(i-1))
                    elif j == 1:
                        row[j][1].set('%f'%sum(subsignal**2))
                    else:
                        percent = (100*sum(subsignal**2)/sum(f**2)).real
                        row[j][1].set('%f %%'%percent)
            else:
                for j in range(3):
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
        
        
        
        if self.mode.get() == 'Cumulative Reconstruction':
            levelsText = "Level(s) -1"+''.join(map(lambda i: '+%i'%i, range(self.level.get()+1)))
            for i in range(self.level.get()+2,len(m)):
                m[i] = [0]*len(m[i])
        else:
            levelsText = "Level %i"%(self.level.get())
            for i in range(len(m)):
                if i != self.level.get()+1:
                    m[i] = [0]*len(m[i])
        s = pywt.waverec(m,self.wavelet.get())
        
        N = len(s)
        t = arange(N)
        F = fft.fft(s)
        F = abs(F[:N/2])
        
        F2 = fft.fft(f)
        F2 = abs(F2[:N/2])
        
        lines = self.lines
        axes = self.axes
        
        lines[0].set_data(t,f)
        lines[1].set_data(w,F2)
        
        lines[2].set_data(t,s)
        lines[3].set_data(w,F)
        
        self.formatAxes(axes[0],t,f,'Time (sec)','Amplitude',self.filename.get())
        self.formatAxes(axes[1],w,F2,'Frequency','Amplitude','FFT of '+self.filename.get())
        self.formatAxes(axes[2],t,s,'Time (sec)','Amplitude',levelsText)
        self.formatAxes(axes[3],w,F,'Frequency','Amplitude','FFT of '+levelsText)
        
        for axis in self.axes:
            axis.get_figure().canvas.draw_idle()
        
if __name__ == "__main__":
    root = Tk()
    MRAWindow(root)
    root.mainloop()  
    
