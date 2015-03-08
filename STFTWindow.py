from FourierWindow import *
from scipy import signal

class STFTWindow(FourierWindow):
        
    def __init__(self, root):
        self.folder = 'signals/'
        self.filenames = os.listdir(self.folder)
    
        FourierWindow.__init__(self, root)
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        '''
        varTitles = ['Plot Type']
        varDTypes = [BooleanVar]
        varDefaults = [False]
        varTexts = [['Plot 2D', 'Plot 3D']]
        varVals = [[False, True]]
        
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        '''
        
        self._makeLeftPane(fileSelector=True)

        #self.plot3D = self.options[0]
        
        l = Label(self.leftPane, text='Windows')
        l.pack(fill=X, pady=(15,0), padx=5)

        dic = {'Modified Bartlett-Hann':'barthann', 'Bartlett':'bartlett', 'Blackman':'blackman', 'Blackman-Harris':'blackmanharris', 
        'Bohman':'bohman', 'Rectangular':'boxcar', 'Dolph-Chebyshev':'chebwin', 'Cosine':'cosine', 'Flat Top':'flattop', 'Hamming':'hamming',
        'Hann':'hann', 'Nutall':'nuttall', 'Parzen':'parzen', 'Triangular':'triang'}
        self.dic=dic
        self.window = StringVar()
        self.window.set('Rectangular')

        windowMenu = OptionMenu(self.leftPane, self.window, *dic.keys(), command=(lambda x: self.updatePlots()))
        windowMenu.config(width=20)
        windowMenu.pack(fill=BOTH,pady=(0,0),padx=5)
                
    
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
        
        self._makeRightPane((2,2), varValues)
        
        self.width = self.vars[0]
        self.center = self.vars[1]
        

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
        l,=axes[0].plot(dummy, color='red')
        lines.append(l)
        self.lines = lines

        self.signalFromFile()

    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    
    def updatePlots(self):
        data = self.signal
        N = len(data)
        t = arange(N)
        delta_w = 2*pi/(N-1)
        w = linspace(0, delta_w*(N/2-1), num=N/2)
        F = abs(fft.fft(data)[:N/2])
        
        width = self.width.get()
        center = self.center.get()
        
        #print width, center, (center-width/2), (N-center-width/2)
        win = eval('signal.%s(%i)'%(self.dic[self.window.get()],width))
        win = np.append(np.append([0]*N,win),[0]*N)
        win = win[N+width/2-center:2*N+width/2-center]
        
        win_data = win*data
        
        win_F = abs(fft.fft(win_data)[:N/2])
        
        lines = self.lines
        axes = self.axes
        
        lines[0].set_data(t,data)
        lines[4].set_data(t,win)
        lines[1].set_data(w,F)
        lines[2].set_data(t,win_data)
        lines[3].set_data(w,win_F)
        
        self.formatAxes(axes[0],t,data,'Time (sec)','Amplitude','Original Signal')
        self.formatAxes(axes[1],w,F,'Frequency','Magnitude','FFT of Original Signal')
        self.formatAxes(axes[2],t,win_data,'Time (sec)','Amplitude','Windowed Signal')
        self.formatAxes(axes[3],w,win_F,'Frequency','Magnitude','FFT of Windowed Signal')

        
        for axis in axes:
            axis.get_figure().canvas.draw_idle()
        
        

    
    
    
