from WaveletWindow import *
from DataGeneratorWindow import *
from MRAWindow import *
from STFTWindow import *
from DIPWindow import *

import os
from ttk import Notebook

root = Tk()
root.wm_title("Signal Processing")
note = Notebook(root)

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
tab4 = Frame(note)
tab5 = Frame(note)

MRAWindow(tab1)
DataGeneratorWindow(tab2)
WaveletWindow(tab3)
STFTWindow(tab4)
DIPWindow(tab5)

note.add(tab4, text = 'Short-Time Fourier Transform')
note.add(tab2, text = 'Data Generator')
note.add(tab3, text = 'Wavelet Analysis')
note.add(tab1, text = 'MRA Decomposition')
note.add(tab5, text = 'Digital Image Processing')
note.pack(fill=BOTH, expand=1)

#w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#root.geometry("%dx%d+0+0" % (w, h))
if os.name == "nt": root.wm_state('zoomed')
else: root.attributes('-zoomed', True)

root.mainloop()
exit()
