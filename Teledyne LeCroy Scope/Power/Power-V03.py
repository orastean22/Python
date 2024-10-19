# ------------------------------------------------
#
# Power Integration - Custom Protocol
#
# Start       1 bit        '0' = 75% Dutycycle
# Payload    27 bits       '1' = 50% Dutycycle
# Stop        1 bit        DataRate 450Kbps
# this version communicate via TCPI with LXI - VISA
#
# ------------------------------------------------
import scope
# imports the pywin32 library for scope connection
import win32com.client

# imports the tkinter library for Window management
from tkinter import *
import string

import pyvisa as visa
import numpy
rm = visa.ResourceManager()
#Set on the Oscilloscope to LXI
lecroy = rm.open_resource("TCPIP0::10.0.0.2::inst0::INSTR") #Instead of IP the Alias can be used (set in NI MAX)

# creates instance of the ActiveDSO control
# scope = win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")

# Connects to the oscilloscope. Substitute your IP address
#scope.MakeConnection("IP:10.0.0.2")   # TSLH 006

#Identify the instrument
print("You are connected to the instrument:\n",lecroy.query("*IDN?"))


# definition of variable
varStr = ""
dataPayloadStr = []
dataPayloadVarStr = ""
dataPayloadLength = 0

# -----------------
# Window management
# -----------------

myWindow = Tk()  # Tk class instance to create the window myWindow
myWindow.title("Data Decoding")  # myWindow Title
myWindow.geometry('810x500')  # myWindow Size

label1 = Label(myWindow, width=50, text="Field Name", font=("Courrier New", 15), fg='black', bg='grey')
label1.grid(column=0, row=0)
label2 = Label(myWindow, width=15, text="Field Value", font=("Courrier New", 15), fg='black', bg='grey')
label2.grid(column=1, row=0)
button = Button(myWindow, width=10, text="    Exit    ", command=myWindow.destroy)
button.grid(column=2, row=0)

label = Label(myWindow, width=50, text="Digitized Temp Signal", font=("Courrier New", 15), fg='white', bg='blue')
label.grid(column=0, row=1, sticky="w")
label = Label(myWindow, width=50, text="Under Voltage Warning", font=("Courrier New", 15), fg='black', bg='white')
label.grid(column=0, row=2, sticky="w")
label = Label(myWindow, width=50, text="Over Voltage Warning", font=("Courrier New", 15), fg='white', bg='blue')
label.grid(column=0, row=3, sticky="w")
label = Label(myWindow, width=50, text="Gate Monitoring Warning", font=("Courrier New", 15), fg='black', bg='white')
label.grid(column=0, row=4, sticky="w")
label = Label(myWindow, width=50, text="OT2_GD Over Temperature Warning", font=("Courrier New", 15), fg='white',
              bg='blue')
label.grid(column=0, row=5, sticky="w")
label = Label(myWindow, width=50, text="OT1_GD Over Temperature Warning", font=("Courrier New", 15), fg='black',
              bg='white')
label.grid(column=0, row=6, sticky="w")
label = Label(myWindow, width=50, text="Secondary Side FluxLink out-of-service Warning", font=("Courrier New", 15),
              fg='white', bg='blue')
label.grid(column=0, row=7, sticky="w")
label = Label(myWindow, width=50, text="Short Circuit Detection Fault", font=("Courrier New", 15), fg='black',
              bg='white')
label.grid(column=0, row=8, sticky="w")
label = Label(myWindow, width=50, text="Parity Bit of Secondary-to-Primary side Communication",
              font=("Courrier New", 15), fg='white', bg='blue')
label.grid(column=0, row=9, sticky="w")
label = Label(myWindow, width=50, text="Primary Side FluxLink out-of-service Warning", font=("Courrier New", 15),
              fg='black', bg='white')
label.grid(column=0, row=10, sticky="w")
label = Label(myWindow, width=50, text="OT1_DCDC Over Temperature Warning", font=("Courrier New", 15), fg='white',
              bg='blue')
label.grid(column=0, row=11, sticky="w")
label = Label(myWindow, width=50, text="OT2_DCDC Over Temperature Warning", font=("Courrier New", 15), fg='black',
              bg='white')
label.grid(column=0, row=12, sticky="w")
label = Label(myWindow, width=50, text="Primary Side DC/DC Controller Over-Current Warning", font=("Courrier New", 15),
              fg='white', bg='blue')
label.grid(column=0, row=13, sticky="w")
label = Label(myWindow, width=50, text="Not Used", font=("Courrier New", 15), fg='black', bg='white')
label.grid(column=0, row=14, sticky="w")
label = Label(myWindow, width=50, text="Dead-Time Insertion Warning", font=("Courrier New", 15), fg='white', bg='blue')
label.grid(column=0, row=15, sticky="w")
label = Label(myWindow, width=50, text="Interlock Warning", font=("Courrier New", 15), fg='black', bg='white')
label.grid(column=0, row=16, sticky="w")

# Data Payload : Row = 1, Column = 6
# scope.WriteString("vbs? 'Return = app.SerialDecode.Out.Result.CellValue(1, 6) '", True)
#lecroy.write("VBS 'Cells = app.SerialDecode.Decode1.Out.Result.CellValue(1, 6) '")
#lecroy.write("VBS? 'Return = Cells(0,0)'")

#dataPayloadStr = bin(int(lecroy.read()) + 2 ** 28)
#dataPayloadLength = len(dataPayloadStr)


# Data Payload : Row = 1, Column = 6
try:
    lecroy.write("VBS 'Cells = app.SerialDecode.Decode1.Out.Result.CellValue(1, 6) '")
    response = lecroy.query("VBS? 'Return = Cells(0,0)'")

    if "Type mismatch" in response:
        raise ValueError("Type mismatch error in VBS command response")

    dataPayloadStr = bin(int(response.strip()) + 2 ** 28)
    dataPayloadLength = len(dataPayloadStr)



    label = Label(myWindow, width=15, text=dataPayloadStr[3:14], font=("Courrier New", 15), fg='white', bg='blue')
    label.grid(column=1, row=1)
    label = Label(myWindow, width=15, text=dataPayloadStr[15], font=("Courrier New", 15), fg='black', bg='white')
    label.grid(column=1, row=2, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[16], font=("Courrier New", 15), fg='white', bg='blue')
    label.grid(column=1, row=3, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[17], font=("Courrier New", 15), fg='black', bg='white')
    label.grid(column=1, row=4, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[18], font=("Courrier New", 15), fg='white', bg='blue')
    label.grid(column=1, row=5, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[19], font=("Courrier New", 15), fg='black', bg='white')
    label.grid(column=1, row=6, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[20], font=("Courrier New", 15), fg='white', bg='blue')
    label.grid(column=1, row=7, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[21], font=("Courrier New", 15), fg='black', bg='white')
    label.grid(column=1, row=8, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[22], font=("Courrier New", 15), fg='white', bg='blue')
    label.grid(column=1, row=9, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[23], font=("Courrier New", 15), fg='black', bg='white')
    label.grid(column=1, row=10, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[24], font=("Courrier New", 15), fg='white', bg='blue')
    label.grid(column=1, row=11, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[25], font=("Courrier New", 15), fg='black', bg='white')
    label.grid(column=1, row=12, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[26], font=("Courrier New", 15), fg='white', bg='blue')
    label.grid(column=1, row=13, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[27], font=("Courrier New", 15), fg='black', bg='white')
    label.grid(column=1, row=14, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[28], font=("Courrier New", 15), fg='white', bg='blue')
    label.grid(column=1, row=15, sticky="w")
    label = Label(myWindow, width=15, text=dataPayloadStr[29], font=("Courrier New", 15), fg='black', bg='white')
    label.grid(column=1, row=16, sticky="w")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    myWindow.mainloop()  # method call to display myWindow
    rm

#myWindow.mainloop()  # method call to display myWindow
#rm.close()
# Disconnects from the oscilloscope
#scope.Disconnect()