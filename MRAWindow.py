from FourierWindow import *
import pywt
from helper_functions import *

class MRAWindow(FourierWindow):
        
    def __init__(self, root):
        self.numLevels=10
        self.signalChanged=True
        
        self.folder = 'signals/'
        self.filenames = os.listdir(self.folder)
    
        FourierWindow.__init__(self, root)
  
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        levelTexts = ['Level %i'%i for i in range(-1,self.numLevels)]
        levelVals = range(-1,self.numLevels)
        
        wavelets = pywt.wavelist()
    
        varTitles = ['Mode', 'Levels']#, 'Wavelets']
        varDTypes = [StringVar, IntVar]#, StringVar]
        varDefaults = ['Cumulative Reconstruction', 7]#, 'db1']
        varTexts = [['Cumulative Reconstruction', 'Arbitrary Reconstruction', 'Decomposition'], levelTexts]#, wavelets]
        varVals = [['Cumulative Reconstruction', 'Arbitrary Reconstruction', 'Decomposition'], levelVals]#, wavelets]
        
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        self._makeLeftPane(optionsSpecs, True)



        l = Label(self.leftPane, text='Wavelets')
        l.pack(fill=X, pady=(30,0), padx=5)

        dic = {'Haar':'haar', 'Daubechies':'db', 'Symlets':'sym', 'Coiflets':'coif', 
            'Biorthogonal':'bior', 'Reverse Biorthogonal':'rbio', 'Discrete Meyer':'dmey'}
        self.dic=dic
        self.family = StringVar()
        self.family.set(dic.keys()[0])
        self.wavelet = StringVar()
        self.wavelet.set(pywt.wavelist(dic[self.family.get()])[0])

        families = OptionMenu(self.leftPane, self.family, *dic.keys(), command=self.updateFamily)
        families.pack(fill=BOTH,pady=(0,0),padx=5)
        wave = OptionMenu(self.leftPane,self.wavelet, *pywt.wavelist(dic[self.family.get()]))
        wave.pack(fill=BOTH, pady=(0,30),padx=5)
        
        self.wave=wave
        
        
        
        self.mode = self.options[0]
        self.level = self.options[1]
        #self.wavelet = self.options[2]
    
    def updateFamily(self,_):
        self.wave['menu'].delete(0,'end')
        for wavelet in pywt.wavelist(self.dic[self.family.get()]):
            self.wave['menu'].add_command(label=wavelet,command=tk._setit(self.wavelet,wavelet))
        self.wavelet.set(pywt.wavelist(self.dic[self.family.get()])[0])
    
    ############################################################################  
    # Contains the plots and frequency sliders at the bottom
    #
    ############################################################################    
    def makeRightPane(self):
    
        self._makeRightPane(2)
        
    ############################################################################  
    # Initializes the signals in the plots
    #
    ############################################################################    
    def initSignals(self):
        axes = self.axes
        lines = [0]*2
        self.lines = lines
        
        dummy = [0]
        lines[0], = axes[0].plot(dummy)
        lines[1], = axes[1].plot(dummy)
        
        self.formatAxes(axes[0],dummy,dummy,'Time (sec)','Amplitude','Original Signal')
        self.formatAxes(axes[1],dummy,dummy,'Frequency','Amplitude','FFT of Signal')
        
        self.signalFromFile()
        
    def updateParams(self):    
        f = self.signal
        N = len(f)
        n = int(log(N)/log(2)+0.5)
        f = np.append(f, [0]*(2**n-N))

        N = 2**n
        
        (A, a) = mra(f, self.numLevels)
        A[0] = mean(A[0])
        
        delta_w = 2*pi/(N-1)
        w = linspace(0, delta_w*(N/2-1), num=N/2)
        
        self.params = [f,A,w,N]
    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    #TODO keep variable of FFT of each level so don't have to compute each time
    def updatePlots(self):
        if self.signalChanged: 
            self.updateParams()
        self.signalChanged = False
        
        [f,A,w,N] = self.params
        
        s = zeros(len(f))
        if self.mode.get() == 'Cumulative Reconstruction':
            for i in range(-1,self.level.get()+1):
                s += A[i+1]
        else: s = A[self.level.get()+1]   

        FF = fft.fft(s)
        FF = abs(FF[:N/2])
        t = arange(N)
        
        lines = self.lines
        axes = self.axes
        lines[0].set_data(t,s)
        lines[1].set_data(w,FF)
        axes[0].axis([0,len(s),min(s),max(s)])
        axes[1].axis([min(w),max(w),min(FF),max(FF)])
        
        
        for axis in self.axes:
            axis.get_figure().canvas.draw_idle()
        
        
        
    def wavedn(f, N):
        M = len(f)
        n = int(log(M)/log(2)+0.5)
        c = d_coeffs[N/2-1]
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
        
    def iwavedn(a, N):
        M = len(a)
        f = [0]*M
        n = int(log(M)/log(2)+0.5)
        c = d_coeffs[N/2-1]
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

    def mra(f, N):
        M = len(f)
        n = int(log(M)/log(2)+0.5)
        MM = 2**n
        if (M > MM):
            f = f[0:MM]
        elif (M < MM):
            f = f + [0]*(MM-M)
        M = MM
        a = wavedn(f,N)
        b = [0]*M
        b[0] = a[0]
        A = []
        A.append(iwavedn(b,N))
        #print A

        for i in range(1,n+1):
            b = [0]*M
            b[2**(i-1):2**i] = a[2**(i-1):2**i]
            #print "b: ",b
            A.append(iwavedn(b,N))
            #raw_input("\n\n\n")
            #print A[i]    

        return (A, a)        
  
    
