from Tkinter import *

master = Tk()

def pipi(a):
    print a

variable = StringVar(master)
variable.set("0") # default value

x = [[str(i), "my option " + str(i)] for i in xrange(100)]
w = OptionMenu(master, variable, *x, command=pipi)
w.pack()

#print variable.get()

mainloop()
