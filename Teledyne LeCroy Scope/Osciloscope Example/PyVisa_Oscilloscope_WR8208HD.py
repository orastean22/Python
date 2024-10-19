"""
Created on Tue Mar 9 12:21:20 2021

@author: sven.kaiser
"""
#import visa
import pyvisa as visa
#import numpy
rm = visa.ResourceManager()
#Set on the Oscilloscope to LXI
lecroy = rm.open_resource("TCPIP0::10.30.82.32::inst0::INSTR") #Instead of IP the Alias can be used (set in NI MAX)

#Identify the instrument
print("You are connected to the instrument:\n",lecroy.query("*IDN?"))
#value = lecroy.read()
#change vertical scale with IEEE 488.2
Gain = "0.5"
lecroy.write("C1:VDIV "+Gain)
#change vertical scale with COM command (VBS ...)
lecroy.write("VBS 'app.Acquisition.C1.VerScale = 1'")
lecroy.write("VBS 'app.SaveRecall.Setup.RecallInternal1'")
lecroy.write("COMM_HEADER OFF")
#lecroy.write("COMM_FORMAT OFF, BYTE, BIN") # set scope to format header off and 1 byte/sample data transfer
lecroy.write("TRMD Normal")
number=4
filename = "Messung_" + str(number) + ".lnb"
lecroy.write("VBS 'app.LabNotebook.SaveFilename = \"D:\\LabNotebook\\"+filename+"\"'")
#scope.WriteString("""VBS 'app.Acquisition.C1.VerScale=".1 V" ' """, 1)
#VBS 'app.LabNotebook.SaveFilename = "D:\LabNotebook\Folder\"'
#Close the VISA resources
#("vbs 'app.SaveRecall.Setup.RecallSetupFilename = \"F:\\Entwicklung\\Vorrichtungen\\- Vorlagen\\LeCroy\\flicker_setup.lss\"'");
rm.close()