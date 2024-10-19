# 
# M.Mastrofini Example of Scope remote control using Python
# September 2017

# C1 is input to filter
# C2 is output from filter
# p1 gain i.e. ration between C2 and C1
# P2 Current frequency
# P3 Amplitude of C1
# P4 Amplitude of C2
# P5 Delta phase C2-C1
# parameters:
# SF start frequency
# EF end frequency
# NM number of measurements - minimum suggested is 10 per decade

SF=10
EF=200000
SFlog10 = int(math.log10(SF))
EFlog10 = int(math.log10(EF))
import win32com.client        #imports the pywin32 library
scope=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")        #creates instance of the ActiveDSO control
scope.MakeConnection("IP:192.168.147.10")       #Connects to the oscilloscope. Substitute your IP address
import math
import numpy
from datetime import datetime
import sys
import os
#import shutil
from time import strftime, localtime, sleep
import matplotlib.pyplot as plt
# set vertical scale and ask for instrument ID with direct commands
scope.WriteString("CHDR off",1)

scope.WriteString("*IDN?",1)
value = "Reading amplitude and frequency values to make a bode plot" 
print (value)
print ("scope model: "+scope.ReadString(80))
scope.WriteString("ARM;WAIT",1)
scope.WriteString("TRMD single",1)

while value != "1":
    scope.WriteString("*OPC?",1)
    value = scope.ReadString(1)
print ("scope armed to use OPC, trigger 20 times")
scope.WriteString("CLSW",1)
#time.sleep(0.2)
# F is the vector containing in first column the frequency, then gain and in 3rd column phase difference
# scope must be set up manually or via setup recall to meet expected results
# phase differences is supposed to be in P5
F = numpy.zeros(shape=(23,3))
scope.WriteString("CLSW",1)
for j in range(0, 23):
    scope.WriteString("ARM;WAIT",1)
    #scope.WriteString("TRMD SINGLE",1)
    opc = 0
    #time.sleep(0.018)
    #wait for acquisition complete
    while opc != "1":
        scope.WriteString("*OPC?",1)
        opc = scope.ReadString(10)
    Command= "VBS? 'return=app.Measure.P1."+'Statistics("Mean")'+".Result.Value'"
    #print ("command sent: "+Command)
    scope.WriteString(Command,1)
    F[j,1]=float(scope.ReadString(50))
    Command= "VBS? 'return=app.Measure.P2."+'Statistics("Mean")'+".Result.Value'"
    scope.WriteString(Command,1)
    F[j,0]=float(scope.ReadString(50))
    Command= "VBS? 'return=app.Measure.P5."+'Statistics("Mean")'+".Result.Value'"
    scope.WriteString(Command,1)
    F[j,2]=float(scope.ReadString(50))
    #print (F[j,0], j)
    scope.WriteString("CLSW",1)
    sys.stdout.write('.'),
print
# convert gain ratio values in dB
for j in range(0, 23):
    F[j,1]= 20*math.log10(F[j,1])
#sort array in order of frequency to plot from 10HZ to 100KHz
F=F[numpy.argsort(F[:,0])]
scope.WriteString("VBS? 'return=app.Acquisition.C1.VerScale",1)
value = scope.ReadString(80)
vertical_Scale= float(value)
scope.WriteString("VBS? 'return=app.Acquisition.Horizontal.HorScale",1)
value = scope.ReadString(80)
T= float(value)

# Gain Plot
fig = plt.figure(figsize=(12, 12))
plt.suptitle("bessel LP filter - 25KHz cutoff ", fontsize=16)
#find max and min in second column for vertical axis range
Imax= numpy.argmax(F[:,1])
Max = F[Imax,1]
Imin= numpy.argmin(F[:,1])
Min = F[Imin,1]
plt.subplot(2,1,1)
plt.semilogx (F[:,0], F[:,1], color="red", linewidth="1.1")
plt.title("gain  - 20Log10(CH2/CH1)", fontsize=16)
plt.ylabel ( "dB")
plt.ylim(Min-5,Max+5)
plt.grid(b=True, which='major', color='b', linestyle='--')
# xlim has Horizontal scale limits, here known to be 10Hz to 10KHz
plt.xlim(100, 110000)

# Phase plot    
sp = plt.subplot(2,1,2)
plt.semilogx (F[:,0], F[:,2], color="red", linewidth="1.1")
plt.title(' Phase CH2 - CH1')
plt.ylabel('Phase - Degrees')
plt.xlabel('frequency')
# ylim is the vertical scale range
plt.ylim(-180,180)
# xlim has Horizontal scale limits, here known to be 10Hz to 10KHz
plt.xlim(100, 110000)
plt.grid(b=True, which='major', color='b', linestyle='--')
plt.show()