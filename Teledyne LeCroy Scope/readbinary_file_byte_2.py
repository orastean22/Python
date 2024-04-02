#
# M.Mastrofini Example of Scope remote control using Python # March 2017
# exaple to read and draw a waveform saved on disk
#
#
from Tkinter import *
from tkFileDialog import askopenfilename
import numpy as np
import time
import os, sys, glob
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt

os.chdir("D:\\waveforms")

def makeWindow () :
    global TextMsg, fig
    win = Tk()
    win.geometry("600x900+750+50")

    frame1 = Frame (win, width=200, height =50)    # Row of buttons
    frame1.pack() 
    b1 = Button(frame1, text=" select TRC file ", command=OpenFile) 
    b1.pack (side=LEFT)
    b2 = Button(frame1, text=" Exit Program ", command=win.quit) 
    b2.pack(side=LEFT)

    frame2 = Frame (win, width=800, height =20)   
    frame2.pack()
    Label(frame2, text="Program Messages").grid(row=0, column=0, sticky=W) 
    frame2.pack_propagate (0)

    frame3 = Frame (win, width=650, height =300)    # select of Technologies
    frame3.pack()
    
    TextMsg = Text (frame3, height=4, width=150, wrap= WORD, state=NORMAL)
    scroll2 = Scrollbar(frame3, orient=VERTICAL)
    scroll2.pack (side=RIGHT, fill=Y)
    TextMsg.pack (side=LEFT, fill=Y)
    scroll2.config (command-TextMsg.yview)
    TextMsg.config(yscrollcommand-scroll2.set)
    TextMsg.insert(END, "please select a Technology and then click on load \n") 
    frame3.pack_propagate(0)

    frame4 = Frame (win)
    frame4.pack()
    fig = plt.figure(1)
    fig.clf(1)
    #global TextMsg, sourcefile, sourcedir, C1
    canvas =  FigureCanvasTkAgg (fig, frame4)
    plot_widget = canvas.get_tk_widget() 
    plot_widget.grid(row=0, column=0)
    
    return win

            # create text widget for program messages

def OpenFile():
    sourcefile = askopenfilename()
    sourcedir = os.path.dirname(sourcefile)


    filesize = os.path.getsize (sourcefile)
    os.chdir(sourcedir)
    if (filesize <10e6) and ("trc" in sourcefile):
        msg = "trace selected is  " + sourcefile + " " 
        + str(int (filesize/1e6)) + "MByte \n"
        #selectfile.configure(fg="green3", bg="gray")
        #TextMsg.delete("1.0", END) TextMsg.insert(END, msg)
        C1 = True
        data = open(sourcefile, "rb").read()
        #first 12 bye need to be discarded #9 and then number of bytes in the
        data = data[11:]
        #start reading from header relevant parameter to draw the waveform 
        Byte_or_Word = int(np. fromstring (data [32], dtype = "uint8")) 
        Voffset = np. fromstring (data [160:164], dtype="float32")[0] 
        Vgain = np. fromstring (data [156:160], dtype="float32")[0] 
        Unit = chr(int (np. fromstring (data [196:197], dtype = "uint8")))
        # WDL WAVEDESC heder lenght usually 346 bytes
        # np. fromstring returns nuple to make it a single value [0] is needed WDL = np.fromstring (data [36:40], dtype = "Int32")[0]
        RL = np.fromstring (data [60: 64], dtype = "Int32")[0]
        NS = np.fromstring (data [174:176], dtype = "int16")[0]
        SampleInterval = np.fromstring (data[176:180], dtype = "float32")[0] 
        Vmax= np.fromstring (data [164: 168], dtype="float32")[0]*Vgain-Voffset 
        Vmin = np.fromstring (data[168:172], dtype="float32") [0] *Vgain-Voffset 
        print ("red from file ", RL," Bytes")
        print ("vertical gain = ", Vgain)
        print ("vertical off set = " , Voffset)
        print ("this wfm is in "+ Unit + "vertical units")
        print ("WaveDesscripotion header is ", WDL, "bytes long")
        print ("top grid level is ", Vmax, Unit )
        print ("bottom grid level is ", Vmin, Unit)

    # Max and Min are returned as int16, need to convert to float to determine vertical scale
    dataword = data[WDL:]
    if (Byte_or_Word == 0):
        print ("this waveform has 8 bit per sample")
        rlen = (RL-2)
        print ("waveform is ", RL-2," sample long")
        data = np.fromstring (dataword [0:rlen], dtype = "int8")
    else:
        print ("this waveform has 16 bit per sample")
        rlen = (RL-4)/2
        print ("waveform is " , rlen, " sample long")
        data = np.fromstring (dataword [0:rlen*2], dtype = "int16")
    if (NS == 1):
        print ("this is not a segmented wfm ")
    else:
        print ("this waveform has", NS, "segments")
        print (" this example program can't manage segmented waveforms" )
        sys.exi()
    
    #find out left and right x axix limits
    
    TO = - SampleInterval * rlen/2
    print ("left x axix Limit", TO )
    T1 = SampleInterval * rlen/2
    print ("right x axix limit", T1)
    # need to calculate x axis horizontal time steps to create x axis
    # hstep is close to SampleInterval, but not identical

    hstep (T1-TO)/rlen
    print (hstep, SampleInterval)
    #X axix vector can be created now 
    x=np.arange(TO, T1, hstep)# 
    #converting now int16 to float 
    data (data * Vgain) - Voffset 
    #define Plot tile, axis, limits 
    #matplotlib.use('TkAgg')
    plt.title("wfm red from file") 
    plt.ylabel(Unit)
    plt.xlabel("time") 
    plt.ylim (Vmin, Vmax)
    plt.xlim(TO, T1) 
    #pltting data
    plt.plot(x, data)
    #fig.canvas.draw() 
    plt.ion()
    #plt.show()
    fig.canvas.draw()
    time.sleep(2)
    fig.clf (1)
    plt.ioff()
if (filesize <350):
    msg= " file too small"+ sourcefile + " " + str(int (filesize/1e3)) + " KByte \n"
    TextMsg.insert(END, msg)
    sourcefileile = " "
    #selectfile.configure(fg="red")
#TextMsg.delete("1.0", END)
else:
    msg=" invalid TRC file or file too big "+ sourcefile + " " + str(int (filesize/1e3)) + " KByte \n"
    sourcefileile = " "
    C1 = False
    #selectfile.configure(fg="red")
    #TextMsg.delete("1.0", END) TextMsg.insert(END, msg)


win =  makeWindow()
#master.title("Select trace you want to draw")
win.mainloop()
plt.clf()
win.destroy()

sys.exit()

