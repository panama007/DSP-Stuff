from FourierWindow import *
from PIL import *

def create_filter(N, r1, r2, filter_type):
    f = np.zeros((N,N), dtype=int)
    for x in range(N):
        for y in range(N):
            r = (x-N/2)**2+(y-N/2)**2
            if filter_type == 0:
                f[x][y] = 1*(r<r1**2)
            elif filter_type == 1:
                f[x][y] = 1*(r>=r1**2)
            elif filter_type == 2:
                f[x][y] = 1*(r<r2**2 and r>=r1**2)
    return f


class DIPWindow(FourierWindow):
        
    def __init__(self, root):
        self.signalType = 1
        
        #self.cwt = {}
        #self.plot3D = 0
    
        FourierWindow.__init__(self, root)
        
    
    def makeLeftPane(self):
        
        varTitles = ['Filter Type']
        varDTypes = [IntVar]
        varDefaults = [0]
        varTexts = [['Low Pass', 'High Pass', 'Band Pass']]
        varVals = [range(3)]
        
        optionsSpecs = [varTitles, varDTypes, varDefaults, varTexts, varVals]
        
        self._makeLeftPane(optionsSpecs, True) 
        
        self.filterType = self.options[0]
        
    def makeRightPane(self):
        varNames = ['Radius 1', 'Radius 2']
        varLimits = [(0,256), (0,256)]
        varRes = [1,1]
        varDTypes = [IntVar,IntVar]
        varDefaults = [0,0]
        varValues = [varNames, varLimits, varRes, varDTypes, varDefaults]
        
        self._makeRightPane((2,2), varValues)
        
        self.r1 = self.vars[0]
        self.r2 = self.vars[1]
        
    def initSignals(self):        
        axes = self.axes
        lines = []
        dummy = [0]
        for axis in axes:
            l,=axis.plot(dummy)
            lines.append(l)

        self.lines = lines

        self.signalFromFile()
        
    def updatePlots(self):
        imag = self.image
        
        axes = self.axes
        
        for axis in axes:
            axis.cla()
                 
        imagF = np.fft.fft2(imag)
        imagF = np.fft.fftshift(imagF)
        imagF2 = np.log10(abs(imagF))
        fil = create_filter(len(imag),self.r1.get(),self.r2.get(),self.filterType.get())
        filtered_imag = abs(np.fft.ifft2(np.fft.ifftshift(fil*imagF)))
        
        
        axes[0].imshow(imag,cmap='gray',vmin=0,vmax=255)
        axes[1].imshow(imagF2,cmap='gray')        
        axes[2].imshow(fil, cmap='gray', vmin=0, vmax=1)
        axes[3].imshow(filtered_imag, cmap='gray')#, vmin=0,vmax=255)

        axes[0].set_title(self.filename.get())
        axes[1].set_title('2D FFT of Image')
        axes[2].set_title('Filter')
        axes[3].set_title('Filtered Image')
        
        
        for fig in self.figs:
            fig.canvas.draw_idle()
            #fig.tight_layout()
 
if __name__ == "__main__":
    root = Tk()
    DIPWindow(root)
    root.mainloop() 