import numpy as np
from numpy import *

import pywt

import os

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D

import Tkinter as tk
import tkFileDialog
from Tkinter import *

from scipy import signal

class FourierWindow(Frame):    
    
    def __init__(self, root):
    
        Frame.__init__(self, root)
        
        self.builtInFunctions = {'Sinusoid' : 'sin(f[0]*2*pi*t)',
                            'Two Sinusoids' : 'sin(f[0]*2*pi*t) + sin(f[1]*2*pi*t)',
                            'Two Seq. Sinusoids' : 'where(t<t[N/2], sin(f[0]*2*pi*t), sin(f[1]*2*pi*t))',
                            'Delta' : 'where(t==t[N/2], 1, 0)',
                            'Chirp' : 'sin((f[0]+(f[1]-f[0])/2*t/t[-1])*2*pi*t)'}
        
        master = PanedWindow(root, orient=HORIZONTAL)
        self.master = master
        master.pack(fill=BOTH, expand=1)

        if self.signalType == 0:
            self.folder = 'signals/'
        else:
            self.folder = 'images/'
        self.filenames = np.sort(os.listdir(self.folder))
        self.len = IntVar()
        self.len.set(-1)
        
        self.makeLeftPane()
        self.makeRightPane()
            
        self.initSignals()
        
           
    def _makeLeftPane(self, optionsSpecs=[], fileSelector=False):
        leftPane = Frame(self.master, bg='grey')
        lleftPane = Frame(leftPane, bg='grey')
        
        if fileSelector:
            filename = StringVar()
            self.filename = filename
            filename.set(self.filenames[-1])
            
            fileSelector = Menubutton(lleftPane,text='Signal Select')

            fileSelector.configure(width=10)
            fileSelector.pack(side=TOP, pady=5, padx=5) 
            
            
            fileSelector.menu = Menu(fileSelector, tearoff=0)
            fileSelector["menu"]  =  fileSelector.menu

            for f in self.filenames:
                fileSelector.menu.add_radiobutton(label=f.replace('.dat',''), 
                    variable=filename, value=f, command=self.signalFromFile)
            
            if self.signalType == 0:
                Label(lleftPane, text='(Negative -> Full Signal)').pack(side=TOP, pady=(5,0), padx=5, fill=BOTH)
                lenSel = Frame(lleftPane)
                Button(lenSel, text='Signal Length', command=self.signalFromFile).pack(side=LEFT, fill=BOTH)
                Entry(lenSel, textvariable=self.len).pack(side=LEFT, fill=BOTH)#, expand=1)
                lenSel.pack(side=TOP, pady=(0,5), padx=5, fill=BOTH)
            
        
        if optionsSpecs:
            [varTitles, varDTypes, varDefaults, varTexts, varVals] = optionsSpecs
            numOptions = len(optionsSpecs[0])

            self.options = []
            self.radioButtons = []

            for i in range(numOptions):
                self.options.append(varDTypes[i]())
                self.options[i].set(varDefaults[i])
            
            for i in range(numOptions):
                self.radioButtons.append([])
            
                l = Label(lleftPane, text=varTitles[i])
                l.pack(fill=X, pady=(5,0), padx=5)

                frame = Frame(lleftPane)
                frame.pack(fill=BOTH,pady=(0,5),padx=5)
                

                for j in range(len(varTexts[i])):
                    rb = Radiobutton(frame, text=varTexts[i][j], variable=self.options[i], value=varVals[i][j], command=self.updatePlots)
                    rb.grid(row=j+1,sticky=W,padx=(5,0))
                    
                    self.radioButtons[i].append(rb)
                        
        lleftPane.grid(row=1,column=1)#,sticky=N+S+E+W)
        #leftPane.columnconfigure(1,weight=1)
        #leftPane.rowconfigure(1,weight=1)
        #leftPane.rowconfigure(2,weight=1)      
        #leftPane.rowconfigure(3,weight=2)  
                
        self.leftPane = leftPane    
        self.master.add(leftPane)    
        
    def _makeRightPane(self, plots, varValues=[]):
        rightPane = Frame(self.master)

        numPlots = plots[0]*plots[1]
        plotFrame = Frame(rightPane)
        plotFrame.pack(fill=BOTH, expand=1)
        plotFrames = [Frame(plotFrame) for i in range(numPlots)] 
        figs = [Figure(figsize=(1,1)) for i in range(numPlots)]
        axes = [fig.add_subplot(111) for fig in figs]
        self.figs = figs
        self.axes = axes
        
        #  creates the matplotlib canvasses for the plots 
        for i in range(numPlots):
            canvas = FigureCanvasTkAgg(figs[i], master=plotFrames[i])
            canvas.show()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
            
        for c in range(plots[1]):
            plotFrame.columnconfigure(c, weight=1)
            for r in range(plots[0]):
                plotFrame.rowconfigure(r, weight=1)
                p = plotFrames[c*plots[1]+r]
                p.grid(row=r, column=c, sticky=N+S+E+W)

        
        # This part below takes care of the sliders. It stores the pointers at
        #   self.sliders and self.vars
        if varValues:
            varsFrame = Frame(rightPane)   
            [varNames, varLimits, varRes, varDTypes, varDefaults] = varValues
            numVars = len(varValues[0])
            
            self.sliders = []
            self.vars = []

            for i in range(numVars):
                self.vars.append(varDTypes[i]()) 
                self.vars[i].set(varDefaults[i])
            
            for i in range(numVars):

                l = Label(varsFrame, text=varNames[i]+': ')
                l.grid(row=i,column=0) 
                w = Scale(varsFrame,from_=varLimits[i][0], to=varLimits[i][1], resolution=varRes[i], 
                    orient=HORIZONTAL, command=(lambda x: self.updatePlots()), variable=self.vars[i])
                w.grid(row=i,column=1, sticky=N+S+E+W)

                self.sliders.append([l,w])
            # only let the sliders expand, labels same size
            varsFrame.columnconfigure(1, weight=1)                       
            varsFrame.pack(fill=X)
               
        self.rightPane = rightPane
        self.master.add(rightPane)
         
    def initSignals(self): pass
    def updatePlots(self): pass

    def formatAxes(self, ax, x, y, xlabel, ylabel, title, spec=False):
        if not spec:
            ax.axis([min(x), max(x), min(y), max(y)])
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        #ax.spines['bottom'].set_position('zero')
        #ax.spines['bottom'].label='zero'
        #ax.xaxis.set_label_coords(0.5,-0.01)
        #ax.yaxis.set_label_coords(-0.05,0.5)
        
    def signalFromFile(self):
        name = self.filename.get()
        if self.signalType == 0:
            with open(self.folder+name, 'rb') as f:
                lines = map(lambda line: line.replace(b'+-', b'-'), f)
                y = loadtxt(lines, dtype=complex128)
            y /= max(abs(y))
            self.funcText = name.replace('.dat', '')
            l = self.len.get()
            if l > 0:
                self.len.set(int(2**ceil(log(l)/log(2))))
            if self.len.get() < 0:
                self.signal = y
            elif self.len.get() < len(y):
                self.signal = y[:self.len.get()]
        else:
            self.image = matplotlib.image.imread(self.folder + name)
        
        self.signalChanged=True
        self.updatePlots()
    
    def parseSignal(self):     
        function = self.funcText.get()
        if function in self.builtInFunctions.keys():
            y = self.builtInFunctions[function]
        else:
            func = self.customFunc.get()
            for i in range(10): func = func.replace('f%i'%i, 'f[%i]'%i)
            y = func
        self.function = y
        
    def hideShowFreqs(self, oldFreqs, newFreqs):
        for i in oldFreqs:
            if i not in newFreqs:
                self.frequencySliders[i][0].grid_remove()
                self.frequencySliders[i][1].grid_remove()
        for i in newFreqs:
            if i not in oldFreqs:
                self.frequencySliders[i][0].grid()
                self.frequencySliders[i][1].grid() 
                
    def file_save(self):
        f = tkFileDialog.asksaveasfilename(defaultextension='.dat', initialdir='signals/', filetypes=[('Data File','.dat')])
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        np.savetxt(f,self.y)
        f.close() # `()` was missing.
    
