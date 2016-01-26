import numpy as np
from numpy import *

import pywt

import os
import time

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D

import Tkinter as tk
import tkFileDialog
from Tkinter import *
from ttk import Notebook

import pyscreenshot as ImageGrab

from scipy import signal

class FourierWindow(Frame):    
    
    def __init__(self, root):
    
        Frame.__init__(self, root)
                
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
        self.pads = [5,15]
        
        self.makeLeftPane()
        self.makeRightPane()
            
        self.initSignals()
        
           
    def _makeLeftPane(self, optionsSpecs=[], fileSelector=False):
        leftPane = Frame(self.master, bg='grey')
        lleftPane = Frame(leftPane, bg='grey')
        
        Button(lleftPane, text='Save Tables and Plots', command=self.saveScreenshot).pack(fill=X, pady=self.pads[1], padx=self.pads[0])
        
        if fileSelector:
            filename = StringVar()
            self.filename = filename
            filename.set(self.filenames[-1])
            
            fileSelector = Menubutton(lleftPane,text='Signal Select')

            fileSelector.configure(width=10)
            fileSelector.pack(side=TOP, pady=self.pads[1], padx=self.pads[0])    
            
            fileSelector.menu = Menu(fileSelector, tearoff=0)
            fileSelector["menu"]  =  fileSelector.menu

            for f in self.filenames:
                fileSelector.menu.add_radiobutton(label=f.replace('.dat',''), 
                    variable=filename, value=f, command=self.signalFromFile)
            
            if self.signalType == 0:
                Label(lleftPane, text='(Negative -> Full Signal)').pack(side=TOP, pady=(self.pads[1],0), padx=self.pads[0], fill=BOTH)
                lenSel = Frame(lleftPane)
                Button(lenSel, text='Signal Length', command=self.signalFromFile).pack(side=LEFT, fill=BOTH)
                Entry(lenSel, textvariable=self.len).pack(side=LEFT, fill=BOTH)#, expand=1)
                lenSel.pack(side=TOP, pady=(0,self.pads[1]), padx=self.pads[0], fill=BOTH)
            
        
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
                l.pack(fill=X, pady=(self.pads[1],0), padx=self.pads[0])

                frame = Frame(lleftPane)
                frame.pack(fill=BOTH,pady=(0,self.pads[1]),padx=self.pads[0])

                for j in range(len(varTexts[i])):
                    rb = Radiobutton(frame, text=varTexts[i][j], variable=self.options[i], value=varVals[i][j], command=self.updatePlots)
                    rb.grid(row=j+1,sticky=W,padx=(self.pads[0],0))
                    
                    self.radioButtons[i].append(rb)
         
        lleftPane.grid(row=1,column=1)
       
        self.leftPane = leftPane   
        self.lleftPane = lleftPane
        self.master.add(leftPane)    
        
    def _makeRightPane(self, plots, varValues=[]):
        rightPane = Frame(self.master)
        y,x = plots[0],plots[1]
        numPlots = x*y
        plotFrame = Frame(rightPane)
        plotFrame.pack(fill=BOTH, expand=1)
        fig = Figure(figsize=(1,1))
        #print y, x, (y-1)*y+(x-1)+1, (x-1)*y+(y-1)+1
        axes = [fig.add_subplot(y,x,i*x+j+1) for i in range(y) for j in range(x)]
        self.fig = fig
        self.axes = axes
        [ax.grid() for ax in axes]
        
        #  creates the matplotlib canvasses for the plots 
        #for i in range(numPlots):
        canvas = FigureCanvasTkAgg(fig, master=plotFrame)
        NavigationToolbar2TkAgg(canvas, plotFrame)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        '''    
        for c in range(plots[1]):
            plotFrame.columnconfigure(c, weight=1)
            for r in range(plots[0]):
                plotFrame.rowconfigure(r, weight=1)
                p = plotFrames[c*plots[1]+r]
                p.grid(row=r, column=c, sticky=N+S+E+W)
        '''
        
        # This part below takes care of the sliders. It stores the pointers at
        #   self.sliders and self.vars
        if varValues:
            self.sliders = [[] for i in range(len(varValues))]
            self.vars = [[] for i in range(len(varValues))]
            varsFrame = Frame(rightPane)
        
            for k in range(len(varValues)):
                   
                [varNames, varLimits, varRes, varDTypes, varDefaults] = varValues[k]
                numVars = len(varValues[k][0])

                for i in range(numVars):
                    self.vars[k].append(varDTypes[i]()) 
                    self.vars[k][i].set(varDefaults[i])
                
                for i in range(numVars):

                    l = Label(varsFrame, text=varNames[i]+': ')
                    l.grid(row=i,column=2*k) 
                    w = Scale(varsFrame,from_=varLimits[i][0], to=varLimits[i][1], resolution=varRes[i], 
                        orient=HORIZONTAL, command=(lambda x: self.updatePlots()), variable=self.vars[k][i])
                    w.grid(row=i,column=2*k+1, sticky=N+S+E+W)

                    self.sliders[k].append([l,w])
                # only let the sliders expand, labels same size
                varsFrame.columnconfigure(2*k+1, weight=1)                       
                varsFrame.pack(fill=X)
               
        self.rightPane = rightPane
        self.master.add(rightPane)
    
    def saveScreenshot(self):
        f = tkFileDialog.asksaveasfilename(defaultextension='.bmp', initialdir='figures/', filetypes=[('Bitmap Image','.bmp')])
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
    
        self.master.config(cursor='none')
        time.sleep(0.05)
        im=ImageGrab.grab(bbox=(0,20,1920,1080-40)) # X1,Y1,X2,Y2
        im.save(f)
        self.master.config(cursor='arrow')
    
    def makeTables(self, headings, frames, heights):
        tables = [[] for i in headings]
        for i in range(len(headings)):
            tableFrame = Frame(frames[i])
            tableFrame.pack(fill=BOTH, pady=5, padx=5)
            
            Label(tableFrame, text=headings[i][0]).grid(row=0,column=0,columnspan=len(headings[i][1]))
            for j in range(len(headings[i][1])):
                Label(tableFrame, text=headings[i][1][j]).grid(row=1,column=j)
                tableFrame.columnconfigure(j, weight=1)
                
            for j in range(heights[i]):
                row = []
                for k in range(len(headings[i][1])):
                    tv = StringVar()
                    l = Label(tableFrame, textvariable=tv)
                    l.grid(row=j+2,column=k,sticky=N+S+E+W)
                    row.append([l,tv])
                tables[i].append(row)
         
        return tables
    
    def freq2ppm(self, freqs):
        return 4.5 - np.array(freqs)*2500/70.45
    
    def updatePeakTable(self, w, F, markersNum, thresholdNum, table, axNum, ppmTable=0, ppmPlot=0):
        numRows = len(table)
        peaks = self.topNPeaks(F, numRows, thresholdNum)
        freqs = [w[p[0]] for p in peaks]
        l = 3
        if ppmTable: 
            ppms = self.freq2ppm(freqs)
            l = 4
        amps = [p[1] for p in peaks]

        if self.markers[markersNum]: 
            try:
                self.markers[markersNum].remove()
            except:
                pass
        if ppmPlot: self.markers[markersNum] = self.axes[axNum].scatter(ppms,amps,marker='x',c='r')
        else: self.markers[markersNum] = self.axes[axNum].scatter(freqs,amps,marker='x',c='r')
        
        for i in range(numRows):
            #print i, len(peaks), peaks
            row = table[i]
            
            if i < len(peaks):
                if not ppmTable:
                    vals = ['#%i'%(i+1),'%f'%freqs[i],'%f'%amps[i]]
                else:
                    vals = ['#%i'%(i+1),'%f'%freqs[i],'%f'%ppms[i],'%f'%amps[i]]
                for j in range(l):
                    row[j][0].grid()
                    row[j][1].set(vals[j])
            else:
                for j in range(l):
                    row[j][0].grid_remove()
                    
    def _initSignals(self, numMarkers=0):
        self.lines = [0]*len(self.axes)
        axes = self.axes
        
        dummy = [0]
        for i in range(len(axes)):
            self.lines[i], = axes[i].plot(dummy)
            
        self.markers = [[]]*numMarkers
        
    
    def initSignals(self): pass
    def updatePlots(self): pass

    def formatAxes(self, ax, x, y, xlabel, ylabel, title, spec=False):
        m = max(np.abs(y))
        if not spec:
            ax.axis([min(x), max(x), min(y)-0.1*m, max(y)+0.1*m])
        else:
            ax.set_ylim([min(y), max(y)])
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        
    def signalFromFile(self):
        name = self.filename.get()
        if self.signalType == 0:
            with open(self.folder+name, 'rb') as f:
                fixes  = [['+-','-'], ['\x00', ''], ['\r\n',''], ['\xff\xfe','']]
                lines = []
                for line in f:
                    temp = line
                    for fix in fixes: temp = temp.replace(fix[0],fix[1])
                    lines.append(temp)
                y = loadtxt(lines, dtype=complex128)
            y /= max(abs(y))
            self.funcText = name.replace('.dat', '')
            self.funcText = name.replace('.txt', '')
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
    
        
    
    
    def topNPeaks(self, data, N, thresholdNum):
        peaks = []
        last = [-1]
        data = last + list(data) + last
        for i in range(len(data)-2):
            try:
                if data[i+1] > data[i] and data[i+1] > data[i+2] and data[i+1] > self.threshold[thresholdNum][0]:
                    peaks.append( (i, data[i+1]) )
            except:
                if data[i+1] > data[i] and data[i+1] > data[i+2]:
                    peaks.append( (i, data[i+1]) )
                
        s = sorted(peaks, key=(lambda x: -x[1]))
        return s[:N]
                
    def file_save(self):
        f = tkFileDialog.asksaveasfilename(defaultextension='.dat', initialdir='signals/', filetypes=[('Data File','.dat')])
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        np.savetxt(f,self.y)
        f.close() # `()` was missing.
    
