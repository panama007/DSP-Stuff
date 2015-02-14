from WaveletWindow import *
from DataGeneratorWindow import *
from MRAWindow import *

from ttk import Notebook

root = Tk()
root.wm_title("Signal Processing")
note = Notebook(root)

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
DataGeneratorWindow(tab2)
MRAWindow(tab1)
WaveletWindow(tab3)

note.add(tab1, text = 'MRA Decomposition')
note.add(tab2, text = 'Data Generator')
note.add(tab3, text = 'Wavelet Analysis')
note.pack(fill=BOTH, expand=1)
root.mainloop()
exit()
