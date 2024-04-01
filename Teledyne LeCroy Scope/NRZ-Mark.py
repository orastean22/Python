#imports the pywin32 library for scope connection
import win32com.client

#imports the tkinter library for Window management
from tkinter import *
import string

#creates instance of the ActiveDSO control
Scope=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")

#Connects to the oscilloscope. Substitute your IP address
Scope.MakeConnection("IP:127.0.0.1")

#definition of variables
TableValue          =["","","","","","","","","","","","","",
"","","","","","","","","","","","","","","","","","","","","","","","","","",""]
StrVariable         =""
SymbolTable         =["","","","","","","",""]
DecodingTable       =["","","","","","","",""]
DecodingData        =""
i_s                 =""
j_s                 =""
NumberOfRow         = 0
NumberOfColumns     = 0
Input               = 0
i                   = 0
j                   = 0
Saisie              = 1

Scope.WriteString("vbs? 'Return = app.SerialDecode.Decode1.Out.Result.Rows'", True)
StrVariable = Scope.ReadString(10)
NumberOfColumns = int(StrVariable)

#-----------------
#Window management
#-----------------

MyWindow = Tk()     #instance de la classe Tk, création de la fenêtre MyWindow
MyWindow.title("Data Decoding") #Titre de la fenêtre MyWindow
MyWindow.geometry('1000x80')

Label1 = Label(MyWindow, width=10, text="Min", font = ("Courrier New",10), fg='black', bg='white')
Label1.grid(column=0, row=0)
Label1 = Label(MyWindow, width=10, text="Row", font = ("Courrier New",10), fg='black', bg='white')
Label1.grid(column=1, row=0)
Label1 = Label(MyWindow, width=10, text="Max", font = ("Courrier New",10), fg='black', bg='white')
Label1.grid(column=2, row=0)
Label2 = Label(MyWindow, width=50, text="Symbol", font = ("Courrier New",10), fg='white', bg='gray')
Label2.grid(column=3, row=0)
Label3 = Label(MyWindow, width=35, text="Data", font = ("Courrier New",10), fg='black', bg='white')
Label3.grid(column=4, row=0)
Label4 = Label(MyWindow, width=10, text="1", font = ("Courrier New",10), fg='black', bg='white')
Label4.grid(column=0, row=1)
Label4 = Label(MyWindow, width=10, text="10", font = ("Courrier New",10), fg='black', bg='white')
Label4.grid(column=2, row=1)

i = 1
while True:    
#-----------------------
#Binary Data downloading    
#-----------------------

j=0    
while j<40:        
i_s = str(i)        
j_s = str(j)

Scope.WriteString("vbs 'Cells = app.SerialDecode.Decode1.Out.Result.CellValue("+i_s+", 5) '", True)        
Scope.WriteString("vbs? 'Return = Cells(0,"+j_s+")'", True)        
StrVariable = Scope.ReadString(10)        
TableValue[j] = StrVariable        
j=j+1


#-------------    
#data decoding    
#-------------

for i in range(8):        
StrVariable = TableValue[i*5] + TableValue[(i*5)+1] + TableValue[(i*5)+2] + TableValue[(i*5)+3] + TableValue[(i*5)+4]        
SymbolTable[i] = StrVariable

for i in range(8):        
if SymbolTable[i] == "11110":
	 DecodingTable[i] = "0x0
	elif SymbolTable[i] ==  "01001":
  	 DecodingTable[i] = "0x1"        
        elif SymbolTable[i] ==   "10100":                
         DecodingTable[i] = "0x2"        
	elif SymbolTable[i] ==   "10101":                
	 DecodingTable[i] = "0x3"        
	elif SymbolTable[i] ==   "01010":                
	 DecodingTable[i] = "0x4"        
	elif SymbolTable[i] ==   "01011":                
	 DecodingTable[i] = "0x5"        
	elif SymbolTable[i] ==   "01110":                
	 DecodingTable[i] = "0x6"        
	elif SymbolTable[i] ==   "01111":                
	 DecodingTable[i] = "0x7"        
	elif SymbolTable[i] ==  "10010":                
	 DecodingTable[i] = "0x8"        
	elif SymbolTable[i] ==   "10011":                
	 DecodingTable[i] = "0x9"        
	elif SymbolTable[i] ==   "10110":                
	 DecodingTable[i] = "0xA"        
	elif SymbolTable[i] ==   "10111":                
	 DecodingTable[i] = "0xB"        
	elif SymbolTable[i] ==   "11010":                
	 DecodingTable[i] = "0xC"        
	elif SymbolTable[i] ==   "11011":                
	 DecodingTable[i] = "0xD"
        elif SymbolTable[i] ==   "11100":                
	 DecodingTable[i] = "0xE"        
	elif SymbolTable[i] ==   "11101":                
	 DecodingTable[i] = "0xF"

Input = Entry(MyWindow, "Row Number ?", width=10)    
Input.grid(column=1, row=1)
i = int(Input.get())

Label5 = Label(MyWindow, width=50, text=SymbolTable, font = ("Courrier New",10), fg='white', bg='gray')    
Label5.grid(column=3, row=1)    
Label6 = Label(MyWindow, width=35, text=DecodingTable, font = ("Courrier New",10), fg='black', bg='white')    
Label6.grid(column=4, row=1)

MyWindow.mainloop()    #cette méthode permet d'afficher la fenêtre MyWindow    
#Disconnects from the oscilloscope
Scope.Disconnect()  