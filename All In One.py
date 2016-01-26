from CWTWindow import *
from DataGeneratorWindow import *
from MRAWindow import *
from STFTWindow import *
from DIPWindow import *
from FSeriesWindow import *
from MRATablePlotsComparisonWindow import *
from CWTTablePlotsComparisonWindow import *

import os
from ttk import Notebook

root = Tk()
root.wm_title("Signal Processing")
note = Notebook(root)

windows = [FSeriesWindow, DataGeneratorWindow, STFTWindow, MRAWindow, CWTWindow, MRAComparisonWindow, CWTComparisonWindow] 

for w in windows:
    tab = Frame(note)
    obj = w(tab)
    note.add(tab, text=obj.title)

note.pack(fill=BOTH, expand=1)

if os.name == "nt": root.wm_state('zoomed')
else: root.attributes('-zoomed', True)

root.mainloop()
exit()
