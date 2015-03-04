import pywt
import matplotlib.pyplot as plt

x = range(100)

m = pywt.wavedec(x, 'db2')

print len(m)
m[-2] = [0]*len(m[-2])

plt.plot(pywt.waverec(m,'db2'))







plt.show()