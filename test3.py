from Tkinter import *

root = Tk()

i = IntVar()
om = OptionMenu(root,i,range(10))
om.config(width=100)

om.pack()

root.mainloop()
