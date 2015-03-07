import matplotlib.pyplot as plt
import numpy as np
import pywt

for j in range(19,20):
    print "hi"
    plt.figure()
    filters = pywt.Wavelet('db%i'%(j+1)).filter_bank

    F = [np.fft.ifft(filters[i]) for i in range(4)]
    F = [F[i][:len(F[i])/2] for i in range(4)]
    F = [np.abs(len(filters[i])*F[i])**2/2 for i in range(4)]

    plt.plot(F[0])
    plt.plot(F[1])
    plt.plot(F[0]**2)
    plt.plot(F[0]+F[1])
plt.show()
