from pylab import *
import pywt
import scipy.io.wavfile as wavfile

ndata = len(data)
self.order=order
self.scale=largestscale
self._setscales(ndata,largestscale,notes,scaling)
self.cwt= NP.zeros((self.nscale,ndata), NP.complex64)
omega= NP.array(range(0,ndata/2)+range(-ndata/2,0))*(2.0*NP.pi/ndata)
datahat=NP.fft.fft(data)
self.fftdata=datahat

for scale in range(maxScale):
    s_omega = omega*scale
    psihat=self.wf(s_omega)
    psihat = psihat *  NP.sqrt(2.0*NP.pi*currentscale)
    convhat = psihat * datahat
    W    = NP.fft.ifft(convhat)
    self.cwt[scaleindex,0:ndata] = W 

