from FourierWindow import *


def wavedn(f, N, wave):
    M = len(f)
    n = int(log(M)/log(2)+0.5)
    c = wave#[N/2-1]
    clr = c[::-1]
    for j in range(0,N,2):
        clr[j] = -clr[j]
    a = list(f)
    for k in range(n,0,-1):
        m = 2**(k-1)
        x = np.zeros(m)
        y = np.zeros(m)
        k2 = [0]*N
        for i in range(m):
            for j in range(N):
                k2[j] = 2*i+j+1;
                while k2[j] > 2*m:
                    k2[j]=k2[j]-2*m
            z = [a[l-1] for l in k2]
            x[i] = np.dot(c,z)
            y[i] = np.dot(clr,z)
        x = x/2
        y = y/2
        a[0:m] = x
        a[m:2*m] = y
    return a
    
def iwavedn(a, N, wave):
    M = len(a)
    f = [0]*M
    n = int(log(M)/log(2)+0.5)
    c = wave#[N/2-1]
    f[0] = a[0]
    c1 = [[0]*(N/2),[0]*(N/2)]
    c2 = [[0]*(N/2),[0]*(N/2)]
    for j in range(N/2):
        c1[0][j] = -c[2*j+1]
        c1[1][j] = c[2*j]
        c2[0][j] = c[N-2*j-2]
        c2[1][j] = c[N-2*j-1]

    for k in range(n):
        m = 2**k;
        k2 = [0]*(N/2)
        x = np.zeros(2*m)
        y = np.zeros(2*m)
        for i in range(m):
            for j in range(N/2):
                k2[j] = m+i-N/2+j+2;
                while k2[j] < m+1:
                    k2[j] = k2[j] + m
            z = [a[l-1] for l in k2]
            x[2*i:2*i+2] = [np.dot(c1[0],z), np.dot(c1[1],z)]
            zz = [f[l-m-1] for l in k2]
            y[2*i:2*i+2] = [np.dot(c2[0],zz), np.dot(c2[1],zz)]
        f[0:2*m] = x+y
    return f

def mra(f, N, wave):
    
    M = len(f)
    n = int(log(M)/log(2)+0.5)
    #print N, n, len(wave)
    MM = 2**n
    f = np.append([0]*(MM-M),f)
    M = MM
    a = wavedn(f,N, wave)
    #print MM,N,len(a)
    b = [0]*M
    b[0] = a[0]
    A = []
    A.append(iwavedn(b,N, wave))

    for i in range(n):
        b = [0]*M
        b[2**i:2**(i+1)] = a[2**i:2**(i+1)]

        A.append(iwavedn(b,N, wave))


    return (A, a)

class MRAWindow(FourierWindow):
        
    def __init__(self, root):
        self.numLevels=10
        self.signalChanged=True
        
        self.folder = 'signals2/'
        self.filenames = os.listdir(self.folder)
    
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
        varTexts = [['Cumulative Reconstruction', 'Arbitrary Reconstruction', 'Decomposition'], levelTexts]
        varVals = [['Cumulative Reconstruction', 'Arbitrary Reconstruction', 'Decomposition'], levelVals]
        
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        self._makeLeftPane(optionsSpecs, True)



        l = Label(self.leftPane, text='Wavelets')
        l.pack(fill=X, pady=(30,0), padx=5)

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
        waveletMenu.pack(fill=BOTH, pady=(0,30),padx=5)
        
        self.waveletMenu=waveletMenu
        
        
        
        self.mode = self.options[0]
        self.level = self.options[1]
        #self.wavelet = self.options[2]
    
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
        
        self.formatAxes(axes[0],dummy,dummy,'Time (sec)','Amplitude','Original Signal')
        self.formatAxes(axes[1],dummy,dummy,'Frequency','Amplitude','FFT of Signal')
        self.formatAxes(axes[2],dummy,dummy,'Time (sec)','Amplitude','Original Signal')
        self.formatAxes(axes[3],dummy,dummy,'Frequency','Amplitude','FFT of Signal')
        
        self.signalFromFile()
        
    def updateParams(self):    
        f = self.signal

        m = pywt.wavedec(f,self.wavelet.get())
        
        N = len(f)
        delta_w = 2*pi/(N-1)
        w = linspace(0, delta_w*(N/2-1), num=N/2)
        
        self.params = [f,w,m]

    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    #TODO keep variable of FFT of each level so don't have to compute each time
    def updatePlots(self):

        #if self.signalChanged: 
        self.updateParams()
        self.signalChanged = False
        
        [f,w,m] = self.params
        #print m[self.level.get()+1]
        
        if self.mode.get() == 'Cumulative Reconstruction':
            for i in range(self.level.get()+2,len(m)):
                m[i] = [0]*len(m[i])
        else: 
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
        axes[0].axis([t[0],t[-1],min(f),max(f)])
        axes[1].axis([min(w),max(w),min(F2),max(F2)])
        
        lines[2].set_data(t,s)
        lines[3].set_data(w,F)
        axes[2].axis([t[0],t[-1],min(s),max(s)])
        axes[3].axis([min(w),max(w),min(F),max(F)])
        
        
        for axis in self.axes:
            axis.get_figure().canvas.draw_idle()
        
  
    
