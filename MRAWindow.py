from FourierWindow import *
from helper_functions import *

class MRAWindow(FourierWindow):
        
    def __init__(self, root):
        self.numLevels=8
        self.signalChanged=True
        
        self.folder = 'signals/'
        self.filenames = os.listdir(self.folder)
    
        FourierWindow.__init__(self, root)
  
  
    ############################################################################  
    # Contains the different options for the signals, using checkboxes
    #
    ############################################################################   
    def makeLeftPane(self):
        levelTexts = ['Level %i'%i for i in range(-1,8)]
        levelVals = range(-1,8)
    
        varDTypes = [StringVar, IntVar]
        varDefaults = ['Cumulative Reconstruction', 7]
        varTexts = [['Cumulative Reconstruction', 'Arbitrary Reconstruction', 'Decomposition'], levelTexts]
        varVals = [['Cumulative Reconstruction', 'Arbitrary Reconstruction', 'Decomposition'], levelVals]
        
        optionsSpecs = [varDTypes, varDefaults, varTexts, varVals]
        
        
        self._makeLeftPane(optionsSpecs, True)
        
        self.mode = self.options[0]
        self.level = self.options[1]
    
    
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
        M = len(f)
        n = int(log(M)/log(2)+0.5)
        MM = 2**n
        if (M > MM):
            f = f[0:MM]
        elif (M < MM):
            f = f + [0]*(MM-M)
        M = MM
        
        (A, a) = mra(f, self.numLevels)
        A[0] = [sum(A[0])/len(A[0])]*len(A[0])
        
        (nRow, nCol) = (len(A), len(A[0])) 
        NN = int(nCol/2. + 0.5)
        delta_w = 2*pi/(nCol-1)
        w = linspace(0, delta_w*(NN-1), num=NN)
        
        self.params = [f,A,w,NN,M]
    ############################################################################  
    # Updates the plots when anything is changed
    #
    ############################################################################       
    #TODO keep variable of FFT of each level so don't have to compute each time
    def updatePlots(self):
        if self.signalChanged: 
            self.updateParams()
        self.signalChanged = False
        
        [f,A,w,NN,M] = self.params
        
        s = zeros(len(f))
        if self.mode.get() == 'Cumulative Reconstruction':
            for i in range(-1,self.level.get()+1):
                s += A[i+1]
        else: s = A[self.level.get()+1]   

        FF = fft.fft(s)
        FF = abs(FF[:NN])
        t = arange(M)
        
        lines = self.lines
        axes = self.axes
        lines[0].set_data(t,s)
        lines[1].set_data(w,FF)
        axes[0].axis([0,len(s),min(s),max(s)])
        axes[1].axis([min(w),max(w),min(FF),max(FF)])
        
        
        for axis in self.axes:
            axis.get_figure().canvas.draw_idle()
        
        
        
        
    s=sqrt(5+2*sqrt(10))
    d_coeffs = np.array([[1., 1.],
                [(1+sqrt(3))/4, (3+sqrt(3))/4, (3-sqrt(3))/4, (1-sqrt(3))/4],
                [(1+sqrt(10)+s)/16, (5+sqrt(10)+3*s)/16, (5-sqrt(10)+s)/8, (5-sqrt(10)-s)/8, (5+sqrt(10)-3*s)/16, (1+sqrt(10)-s)/16],
                [.325803428051, 1.010945715092, .892200138246, -.039575026236, -.264507167369, .043616300475, .046503601071, -.014986989330],
                [.226418982583, .853943542705, 1.024326944260, .195766961347, -.342656715382, -.045601131884, .109702658642, -.008826800109, -.017791870102, .004717427938],
                [.157742432003,.699503814075,1.062263759882,.445831322930,-.319986598891,-.183518064060,.137888092974,.038923209708,-.044663748331,.000783251152,.006756062363,-.001523533805],                [.110099430746,.560791283626,1.031148491636,.664372482211,-.203513822463,-.316835011281,.100846465010,.114003445160,-.053782452590,-.023439941565,.017749792379,.000607514996,-.002547904718,.000500226853],
                [.076955622108,.442467247152,.955486150427,.827816532422,-.022385735333,-.401658632782,.000668194093,.182076356847,-.024563901046,-.062350206651,.019772159296,.012368844819,-.006887719256,-.000554004548,.000955229711,-.000166137261],
                [.053850349589,.344834303815,.855349064359,.929545714366,.188369549506,-.414751761802,-.136953549025,.210068342279,.043452675461,-.095647264120,.000354892813,.031624165853,-.006679620227,-.006054960574,.002612967280,.000325814672,-.000356329759,.000055645514],
                [.037717157593,.266122182794,.745575071487,.973628110734,.397637741770,-.353336201794,-.277109878720,.180127448534,.131602987102,-.100966571196,-.041659248088,.046969814097,.005100436968,-.015179002335,.001973325365,.002817686590,-.000969947840,-.000164709006,.000132354366,-.000018758416]])

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
  
    
