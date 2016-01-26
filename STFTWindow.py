from FourierWindow import *
from scipy import signal

class STFTWindow(FourierWindow):
        
    def __init__(self, root):
        self.title = 'Short-Time Fourier Transform'
        
        self.signalType = 0
    
        FourierWindow.__init__(self, root)
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        
        varTitles = ['FFT Plot Type']
        varDTypes = [BooleanVar]
        varDefaults = [False]
        varTexts = [['Stem Plot', 'Normal Line Plot']]
        varVals = [[True, False]]
        
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        
        self._makeLeftPane(optionsSpecs,fileSelector=True)

        self.fftPlot = self.options[0]
        
        extraOptions = Frame(self.leftPane, bg='grey')
        extraOptions.grid(row=2, column=1, sticky=N+S+E+W)
        tableFrame1 = Frame(self.leftPane, bg='grey')
        tableFrame1.grid(row=3,column=1,sticky=N+S+E+W, pady=self.pads[1], padx=self.pads[0])
        tableFrame2 = Frame(self.leftPane, bg='grey')
        tableFrame2.grid(row=4,column=1,sticky=N+S+E+W, pady=self.pads[1], padx=self.pads[0])
        
        titlePane = Frame(extraOptions)
        titlePane.pack(fill=X, pady=(self.pads[1],0), padx=self.pads[0])
        
        Label(titlePane, text='Windows').pack(fill=BOTH, side=LEFT, expand=1)
        #Button(titlePane, text='?', command=self.popupWindow).pack(fill=BOTH, side=LEFT)

        dic = {'Modified Bartlett-Hann':'barthann', 'Bartlett':'bartlett', 'Blackman':'blackman', 'Blackman-Harris':'blackmanharris', 
        'Bohman':'bohman', 'Rectangular':'boxcar', 'Cosine':'cosine', 'Flat Top':'flattop', 'Gaussian':'gaussian', 'Mexican Hat':'ricker',
        'Hamming':'hamming','Hann':'hann', 'Nutall':'nuttall', 'Parzen':'parzen', 'Triangular':'triang'}
        self.dic=dic
        self.window = StringVar()
        self.window.set('Rectangular')

        windowMenu = OptionMenu(extraOptions, self.window, *dic.keys(), command=(lambda x: self.updatePlots()))
        #windowMenu.config(width=20)
        windowMenu.pack(fill=BOTH,pady=(0,self.pads[1]),padx=self.pads[0])
        
        headings = [("Frequency Peaks in Original Signal", ["Peak", "Frequency", "Amplitude"]),
                    ("Frequency Peaks in Windowed Signal", ["Peak", "Frequency", "Amplitude"])]
        frames = [tableFrame1, tableFrame2]
        heights = [10,10]
        
        [self.peaksOrigTable, self.peaksWindTable] = self.makeTables(headings, frames, heights)
                
    def popupWindow(self):
        popup = Toplevel()
        fig = Figure(figsize=(5,5))
        ax0 = fig.add_subplot(211)
        ax1 = fig.add_subplot(212)

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.show()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        
        win = eval('signal.%s(%i)'%(self.dic[self.window.get()],self.width.get()))
        ax0.plot(win)
        self.formatAxes(ax0,range(self.width.get()),win,'Sample','Amplitude',self.window.get())
        
        F = np.fft.fftshift(abs(np.fft.fft(win,2048)))
        F = 10*np.log10(F[1024-40:1024+41])
        freqs = range(-len(F)/2,len(F)/2)
        ax1.plot(freqs,F)
        self.formatAxes(ax1,freqs,F,'FFT Bin','Decibels','Fourier Transform')
        
        fig.tight_layout()
        
    def mouseCallback1(self, event, thresholdNum, axisNum):
        s = self.axes[1].format_coord(event.xdata,event.ydata)
        
        yind1 = s.find('y')
        yind2 = yind1 + s[yind1:].find(' ')
        y = float(s[yind1+2:yind2])
        
        [w,F] = self.Fplot[thresholdNum]
        
        if event.button == 1:
            if self.threshold[thresholdNum][1]: self.threshold[thresholdNum][1].pop(0).remove()
            
            self.threshold[thresholdNum][0] = y
            self.threshold[thresholdNum][1] = self.axes[axisNum].plot(w,[y]*len(w), color='k', linewidth=2)
            
        elif event.button == 3:
            if self.threshold[thresholdNum][1]: self.threshold[thresholdNum][1].pop(0).remove()
            
            self.threshold[thresholdNum][0] = None
            
        peakTable = self.peaksOrigTable if thresholdNum == 0 else self.peaksWindTable
        self.updatePeakTable(w,F,thresholdNum,thresholdNum,peakTable,axisNum)
        self.axes[axisNum].get_figure().canvas.draw_idle()
            
    def mouseCallback(self, event):   
        #print event.ydata
        if (bool(event.ydata) & (event.inaxes == self.axes[1])):
            self.mouseCallback1(event,0,1)
        if (bool(event.ydata) & (event.inaxes == self.axes[3])):
            self.mouseCallback1(event,1,3)
        
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
        varNames = ['Width', 'Center']
        varLimits = [(1,1024), (0,1024)]
        varRes = [1,1]
        varDTypes = [IntVar,IntVar]
        varDefaults = [10,0]
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane((2,2), [varValues])
        
        self.width = self.vars[0][0]
        self.center = self.vars[0][1]
        

    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):
        self._initSignals(numMarkers=2)
        
        l,=self.axes[0].plot([0], color='red')
        self.lines.append(l)
        
        self.fig.canvas.mpl_connect('button_press_event', self.mouseCallback)
        self.threshold = [[None]*2]*2

        self.signalFromFile()

    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    
    def updatePlots(self):
        data = self.signal
        N = len(data)
        
        t = np.arange(N)
        delta_w = 1./(N-1)
        w = np.linspace(0, delta_w*(N/2-1), N/2)
        F = np.abs(np.fft.fft(data)[:N/2])
        
        width = self.width.get()
        center = self.center.get()
        
        #print width, center, (center-width/2), (N-center-width/2)
        window = self.dic[self.window.get()]
        if window == 'gaussian':
            win = eval('signal.%s(%i,%f)'%(window,width,width/10.))
        elif window == 'ricker':
            a = width/10.
            win = eval('signal.%s(%i,%f)'%(window,width,a))
        else:
            win = eval('signal.%s(%i)'%(window,width))
        win = np.append(np.append([0]*N,win),[0]*N)
        win = win[N+width/2-center:2*N+width/2-center]
        
        win_data = win*data
        
        win_F = abs(fft.fft(win_data)[:N/2])
        
        lines = self.lines
        axes = self.axes
        
        lines[0].set_data(t,data)
        lines[4].set_data(t,win)
        #lines[1].set_data(w,F)
        lines[2].set_data(t,win_data)
        #lines[3].set_data(w,win_F)
        
        axes[1].cla()
        axes[1].grid()
        axes[3].cla()
        axes[3].grid()
        if self.fftPlot.get():
            axes[1].stem(w,F,basefmt='k:')
            axes[3].stem(w,win_F,basefmt='k:')
        else:
            axes[1].plot(w,F)
            axes[3].plot(w,win_F)
            
        mean = sum([amp*freq for (freq, amp) in zip(w, F)])/sum(F)
        midpoint = sum(F)/2.
        cur = 0
        for ind in range(len(w)):
            cur += F[ind]
            if cur >= midpoint:
                median = w[ind]
                break
        stddev = (sum([(freq-mean)**2*amp for (freq,amp) in zip(w, F)])/sum(F))**0.5
        
        loc = [min(w) + (max(w)-min(w))*0.7, min(F) + (max(F)-min(F))*0.9]
        axes[1].text(loc[0],loc[1],'Mean: %0.5f\nMedian: %0.05f\nStd. Dev: %0.05f'%(mean,median,stddev),bbox={'facecolor':'white','alpha':1,'pad':10})
        
        mean = sum([amp*freq for (freq, amp) in zip(w, win_F)])/sum(win_F)
        midpoint = sum(win_F)/2.
        cur = 0
        for ind in range(len(w)):
            cur += win_F[ind]
            if cur >= midpoint:
                median = w[ind]
                break
        stddev = (sum([(freq-mean)**2*amp for (freq,amp) in zip(w, win_F)])/sum(win_F))**0.5
        
        loc = [min(w) + (max(w)-min(w))*0.7, min(win_F) + (max(win_F)-min(win_F))*0.9]
        axes[3].text(loc[0],loc[1],'Mean: %0.5f\nMedian: %0.05f\nStd. Dev: %0.05f'%(mean,median,stddev),bbox={'facecolor':'white','alpha':1,'pad':10})
         
        self.Fplot = [[w,F],[w,win_F]]
        self.updatePeakTable(w,F, 0, 0, self.peaksOrigTable, 1)
        self.updatePeakTable(w,win_F, 1, 1, self.peaksWindTable, 3)
        
        yscale = [min(min(data),min(win)), max(max(data),max(win))]
        self.formatAxes(axes[0],t,yscale,'Time (ms)','Amplitude',self.filename.get())
        self.formatAxes(axes[1],w,F,'Frequency (kHz)','Magnitude','FFT of '+self.filename.get())
        self.formatAxes(axes[2],t,win_data,'Time (ms)','Amplitude','Windowed Signal')
        self.formatAxes(axes[3],w,win_F,'Frequency (kHz)','Magnitude','FFT of Windowed Signal')

        self.sliders[0][0][1].config(to=len(data)/2)
        self.sliders[0][1][1].config(to=len(data))
        
        [ax.axhline(color='k') for ax in self.axes]
        #for fig in self.figs:
        self.fig.canvas.draw_idle()
        #self.fig.tight_layout()
        
if __name__ == "__main__":
    root = Tk()
    STFTWindow(root)
    
    if os.name == "nt": root.wm_state('zoomed')
    else: root.attributes('-zoomed', True)

    root.mainloop()        

    
    
    
