#
# M.Mastrofini Example of Scope remote control using Python
#  July 2014 -  ver 1.0
# example using direct commands and VBS commands
#  Wincom extension must be installed#import win32com.client 
# 
import win32com.client #imports the pywin32 library   
#from GimpGradientFile import SEGMENTS
scope=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")  #creates instance of the ActiveDSO control
scope.MakeConnection("IP:192.168.147.102") #Connects to the oscilloscope.  Substitute your IP address
import re
import binascii
import functools
import time
from Tkinter import *
from tkFileDialog   import askopenfilename  
import numpy as np
import time
import os, sys, glob
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
global select, SourceVar, CMDVar, b1, b2
Sourcelist = [           
            ['C1','app.Acquisition.C1.Out.Result'],           
            ['C2','app.Acquisition.C2.Out.Result'],           
            ['C3','app.Acquisition.C3.Out.Result'],           
            ['C4','app.Acquisition.C4.Out.Result'],           
            ['F1', 'app.Math.F1.Out.Result'],           
            ['F2', 'app.Math.F2.Out.Result'],           
            ['F3', 'app.Math.F3.Out.Result'],           
            ['F4', 'app.Math.F4.Out.Result'],           
            ['M1','app.Memory.M1.Out.Result'],           
            ['M2','app.Memory.M2.Out.Result'],           
            ['M3','app.Memory.M3.Out.Result'],           
            ['M4','app.Memory.M4.Out.Result'],           
            ['Z1','app.Zoom.Z1.Out.Result'],           
            ['Z2','app.Zoom.Z2.Out.Result'],           
            ['Z3','app.Zoom.Z3.Out.Result'],           
            ['Z4','app.Zoom.Z4.Out.Result']           
            ]
          
def whichSelected () :    
    #returns index  to actual selected row of selected item    
    #print "At %s of %d" % (select.curselection(), len(Sourcelist))    
    return int(select.curselection()[0])

def setSelect () :    
    Sourcelist.sort()    
    select.delete(0,END)    
    for Source, CMD in Sourcelist :        
        select.insert (END, Source)        

def makeWindow () :    
    #2 gloabla variable used in openfile()    
    global TextMsg, fig, select, SourceVar, CMDVar, b1, b2    
    #call to tk()    
    win = Tk()    
    # x width, y hight; +x start, +y start - from upper left corner    		

    win.geometry("900x900+100+100")    
    frame1 = Frame(win)    
    frame1.pack()        
    
    Label(frame1, text="Trace Source ").grid(row=0, column=0, sticky=W)    
    SourceVar = StringVar()        
    
    Source = Entry(frame1, width=100, textvariable=SourceVar)    
    Source.grid(row=0, column=1, sticky=W)    
    
    Label(frame1, text="Scope Command").grid(row=1, column=0, sticky=W)    
    CMDVar= StringVar()    
    CMD = Entry(frame1, width= 100, textvariable=CMDVar)    
    CMD.grid(row=1, column=1, sticky=W)    
    frame1.pack_propagate(0)       
      
    frame2 = Frame(win, width=300, height =50)       #2  buttons needed, select file and exit program    
    frame2.pack()    
    b1 = Button(frame2,text=" select trace source ",command=Load_Source) # open file bitton    
    b1.pack(side=LEFT)    
    b2 = Button(frame2,text=" Get trace ",command=Get_trace)    # exit program button    
    b2.pack(side=LEFT)    
    b3 = Button(frame2,text=" Exit Program ",command=win.quit)    # exit program button    
    b3.pack(side=LEFT)            
    
#propagate is required to activate non default frame size      
      
    frame3 = Frame(win, width=800, height = 80)           
    frame3.pack()    
    scroll = Scrollbar(frame3, orient=VERTICAL)    
    select = Listbox(frame3, yscrollcommand=scroll.set, height=6)    
    scroll.config (command=select.yview)    
    scroll.pack(side=RIGHT, fill=Y)    
    select.pack(side=LEFT,  fill=BOTH, expand=1)    
    frame3.pack_propagate(0)    
    frame2.pack_propagate(0)    
    # simple label for text message window
            
    # frame for actual text message window    
    frame4 = Frame(win, width=800, height =200)       # select of Technologies    
    frame4.pack()    
    TextMsg = Text(frame4, height=4, width=150, wrap= WORD, state=NORMAL)    
    # frame type with scroll  bar on the right    
    scroll2 = Scrollbar(frame4, orient=VERTICAL)    
    scroll2.pack(side=RIGHT, fill=Y)    
    TextMsg.pack(side=LEFT, fill=Y)    
    scroll2.config(command=TextMsg.yview)    
    TextMsg.config(yscrollcommand=scroll2.set)    
    TextMsg.insert(END, "please select the trace to draw \n")    
    frame4.pack_propagate(0)    
    # frame where plot will be shown    
    frame5 = Frame(win, width=800, height =500)    
    frame5.pack()    
    # create the figure object and clear it to close the plot window outside Tk    
    fig = plt.figure(1)    
    fig.clf(1)    
    #thes lines create the actual figure in Tk    
    canvas = FigureCanvasTkAgg(fig, frame5)		
    plot_widget = canvas.get_tk_widget()    
    plot_widget.grid(row=0, column=0)    
    # without this line will not work, why not clear    
    return win

def setSelect () :
    Sourcelist.sort()    
    select.delete(0,END)    
    for Source, CMD in Sourcelist :        
            select.insert (END, Source)        
def Load_Source ():    
    Source, CMD = Sourcelist[whichSelected()]    
    SourceVar.set(Source)    
    b1.configure(fg="black", bg="gray")    
    b2.configure(fg="spring green", bg="gray1")    
    CMDVar.set(CMD)    
    i=whichSelected()    
    S1= Sourcelist[i][0]    
    S2=Sourcelist[i][1]    
    win.update()    
    msg = "VBS? 'return="+S2+".Sweeps'"    
    scope.WriteString(msg,1)    
    value =scope.ReadString(20)    
    #print value    
    rules = [value =="No Data Available", 
             value =="0",
             value =="" ]    
    if any(rules) :
        TextMsg.delete("1.0", END)
        msg =  "\nselected source trace  " + S1 + " is not available \nselect another source trace"        
        b1.configure(fg="green", bg="gray")        
        b2.configure(fg="red", bg="gray10", state="disabled")        
        TextMsg.insert(END, msg)        
        win.update()    
    else:        
        TextMsg.delete("1.0", END)        
        msg =  "\nselected source trace  " + S1 + " is available \nselect Get Trace to plot waveform"        
        TextMsg.insert(END, msg)        
        b1.configure(fg="white", bg="gray1")        
        b2.configure(fg="spring green", bg="gray", state="normal")        
        win.update()
def Get_trace():    
        # this function opens the file, set default directory, prints messages, downsamples with peak detect wfm and plots it    
        # plot function has limited resolution (2 Mpoints I believe) in any case is better to reduce the actual drawn point    
        i=whichSelected()    
        S1= Sourcelist[i][0]    
        S2=Sourcelist[i][1]    
        b1.configure(fg="black", bg="gray")    
        b2.configure(fg="green", bg="white")    
        msg = "VBS? 'return="+S2+".Sweeps'"    
        scope.WriteString(msg,1)    
        value =scope.ReadString(20)    
        #print value    
        rules = [value =="No Data Available",
                 value =="0",
                 value =="" ]
        if any(rules) :        
            TextMsg.delete("1.0", END)
            msg =  "\nselected source trace  " + S1 + " is not available \n"        
            b1.configure(fg="green", bg="white")        
            b2.configure(fg="red", bg="gray")        
            TextMsg.insert(END, msg)        
            win.update()    
        else:
            Sweeps = int(value)
            plt.title(S1)
            msg =  "selected source trace  " + S1 + " \n"
            b1.configure(fg="black", bg="gray")
            b2.configure(fg="green", bg="gray")
            TextMsg.delete("1.0", END)
            TextMsg.insert(END, msg)
            win.update()
            scope.WriteString("TRMD STOP",1)
            value = ""
            scope.WriteString("TRMD?",1)
            msg = msg + scope.ReadString(80) +"\n"
            while value != "STOP":
                scope.WriteString("TRMD?",1)
                value = scope.ReadString(80)
            scope.WriteString("COMM_HEADER OFF",1)
            scope.WriteString("COMM_FORMAT DEF9,Word,Bin",1)
            cmd = S1 +":WF? DAT1"
            scope.WriteString(cmd,1)
            header = scope.ReadBinary(16)
            #print (header)
            rlen = int(header[7:16])-4
            dataword = scope.ReadBinary(rlen)
            dataword =  np.fromstring(dataword, dtype=np.int16)
            RL = rlen/2
            header = scope.ReadBinary(4) # read last 4 bytes left in the buffer
            msg = "VBS? 'return="+S2+".VerticalUnits'"
            scope.WriteString(msg,1)
            Vunit = scope.ReadString(80)
            msg = "VBS? 'return=" + S2+ ".VerticalPerStep'"
            scope.WriteString(msg,1)
            value = scope.ReadString(80)
            VerticalStep= float(value)
            msg = "VBS? 'return=" + S2+ ".VerticalOffset'"
            scope.WriteString(msg,1)
            value = scope.ReadString(80)
            Voffset= float(value)
            #msg = "VBS? 'return=" + S2+ ".VerticalMinPossible'"
            ###scope.WriteString(msg,1)
            ##value = scope.ReadString(80)
            #Vmin= float(value)        
            msg = "VBS? 'return=" + S2+ ".VerticalFrameStart'"        
            scope.WriteString(msg,1)        
            value = scope.ReadString(80)        
            Vmin= float(value)        
            msg = "VBS? 'return=" + S2+ ".VerticalFrameStop'"        
            scope.WriteString(msg,1)        
            value = scope.ReadString(80)        
            Vmax= float(value)               
            msg = "VBS? 'return=" + S2+ ".HorizontalUnits'"        
            scope.WriteString(msg,1)        
            Hunit = scope.ReadString(80)        
            msg = "VBS? 'return=" + S2+ ".HorizontalFrameStart'"        
            scope.WriteString(msg,1)        
            value = scope.ReadString(80)        
            T0= float(value)        
            msg = "VBS? 'return=" + S2+ ".HorizontalFrameStop'"        
            scope.WriteString(msg,1)		
            
            value = scope.ReadString(80)        
            T1= float(value)          
            msg = "VBS? 'return=" + S2+ ".HorizontalPerStep'"        
            scope.WriteString(msg,1)        
            value = scope.ReadString(80)        
            SampleInterval= float(value)        
            timewindow = T1-T0        
            #read first 15 bytes, to determine how many bytes need to be transferred         

            Vertical_Scale=VerticalStep*8192                

            #start reading from header relevant parameter to draw the waveform        
            msg =  "red from scope "+ str(rlen) + " Bytes \n"        
            msg = msg + "vertical scale = " + str() + "\n"
            msg = msg + "vertical off set = " + str(Voffset) +"\n"
            msg = msg +  "Vertical unit is "+ Vunit + " \n"
            msg = msg + "Horizontal unit is "+ Hunit +"\n"
            msg = msg + "top grid level is "+ str(Vmax) +Vunit +"\n"
            msg = msg + "bottom grid level is "+ str(Vmin) +  Vunit + "\n" 
            TextMsg.insert(END, msg) 
            win.update()        
            # VMax and VMin are returned as int16,  need to convert to float to determine vertical scale                

            segments = int(len(dataword)/250)                            

            if segments <500:            
                segments = 500        
            msg =  "Vertical scale is 16 bit  per sample"        
            points_in_segment=int(RL/(segments))        
            msg = msg +  ", "+ str(RL/1000) + " Ksample \n"        
            msg= msg + "Trace is drawn using a "+ str(points_in_segment) + "x decimation factor \n"        
            msg = msg + "trace horizzontal time windows is " + str(timewindow) + "s \n"        
            
            TextMsg.insert(END, msg)        
            win.update()        
            data =np.zeros(segments*2)        
            # A better algorithm can be found to make sure we have a number of points_in_segment        
            # which is an integer sub-multiple of the record length rlen
            # N pixels available, N/2 for max and N/2 for min        
    
            for k in range(0,segments-1):            
                #print k*points_in_segment, (k+1)*points_in_segment,k            
                subdata = dataword[(k)*points_in_segment:(k+1)*points_in_segment]                        
        
                #print len(subdata)          
            # in each segment search max and min value, and index of them in the vector            
                Imax= np.argmax(subdata)            
                Max = subdata[Imax]            
                Imin= np.argmin(subdata)            
                Min = subdata[Imin]            
                #print (Max, Imax, Min, Imin, 2*k, 2*k+1, segments-k)        
            #decide waht comes first in plot Min or Max            
                if Imax > Imin:
                    data[2*k]= Min
                    data[2*k+1] =Max
                else:
                    data[2*k]= Max
                    data[2*k+1] = Min
            T0=0
            msg =  "axis Limits:  X left = "+ str(T0)+ Hunit
            T1=SampleInterval * RL
            msg =  msg + " -  X right  = " + str(T1) + Hunit
            TextMsg.insert(END, msg)
            win.update()
            fig.clf(1)
            # need to calculate x axis horizontal  time steps to create x axis vector
            #hstep is close to SampleInterval, but not identical
            hstep=(T1-T0)/len(data)
            #print (T1-T0)/hstep, 
            #X axix vector can be created now
            x=np.arange(T0, T1, hstep)
            # randomly x()  is 1 point longer than data() probably because of the way np.arange(T0, T1, hstep) is constructed
            # control on length of these 2 vector is required to avoid error message
            if len(x)>len(data):
                x = x[0:len(x)-1]
            #print len(x), len(data), T1-T0, hstep,
            #converting now int16 to float
            data = (data*Vertical_Scale/8192) 
            data = data + Voffset
            plt.ylabel(Vunit)
            plt.xlabel(Hunit)
            #print Vmin - abs(0.1*Vmin), Vmax + abs(0.1*Vmax)
            plt.ylim(Vmin, Vmax)
            plt.xlim(T0, T1)
            #pOltting data
            plt.plot(x,data)
            #fig.canvas.draw()
            plt.ion()
            #plt.show()
            fig.canvas.draw()
        
        
            plt.ioff()
        b1.configure(fg="black", bg="gray")    
       
win = makeWindow()
setSelect ()
win.mainloop()
plt.clf()
win.destroy()
# 
exit()



	
