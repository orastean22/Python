##################################### 
# Trigger Pattern on UART with read of the first acquired frame
# LB 2024
# 
####################################

#imports the pywin32 library for scope connection
import win32com.client

#creates instance of the ActiveDSO control
scope=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")

#Connects to the oscilloscope. Substitute your IP address
scope.MakeConnection("IP:192.168.1.6")

#definition of variables
intVar      = 0
strVar      =""
asciiVar    = 0
i           = 0
str_i       =""
dataFrame   =""

scope.WriteString("""vbs 'app.Acquisition.TriggerMode="Stopped"' """, True)
scope.WriteString("vbs 'app.SaveRecall.Setup.DoRecallDefaultPanel' ", True)
scope.WriteString("vbs 'app.Acquisition.C2.View=0' ", True)

# Acquisition Time configuration
scope.WriteString("vbs 'app.Acquisition.Horizontal.HorScale=10e-3' ", True)
scope.WriteString("vbs 'app.Acquisition.Horizontal.HorScale=10e-3' ", True)
scope.WriteString("vbs 'app.Acquisition.Horizontal.HorOffset=-40e-3' ", True)

# Channel 1 configuration
scope.WriteString("vbs 'app.Acquisition.C1.VerScale=500e-3' ", True)
scope.WriteString("vbs 'app.Acquisition.C1.VerOffset=-1.5' ", True)
# Zoom 1 configuration
scope.WriteString("""vbs 'app.Zoom.Z1.Source="C1"' """, True)
scope.WriteString("vbs 'app.Zoom.Z1.Zoom.HorCenter=-1e-3' ", True)
scope.WriteString("vbs 'app.Zoom.Z1.Zoom.HorScale=500e-6' ", True)
scope.WriteString("vbs 'app.Zoom.Z1.Zoom.VerCenter=2' ", True)
scope.WriteString("vbs 'app.Zoom.Z1.Zoom.VerScale=1' ", True)
scope.WriteString("vbs 'app.Zoom.Z1.View=1' ", True)

# Serial Decode 1 configuration
#    - UART    
#    - C1    
#    - Message Frame    
#    - 100 Kbps    
#    - ASCII    
#    - InterFrame 2ms
#    - LSB
#    - IdleHigh

scope.WriteString("""vbs 'app.SerialDecode.Decode1.Protocol="UART"' """, True)
scope.WriteString("""vbs 'app.SerialDecode.Decode1.Src1="C1"' """, True)
scope.WriteString("""vbs 'app.SerialDecode.Decode1.Decode.ModeSetup="MessageFrame"' """, True)
scope.WriteString("vbs 'app.SerialDecode.Decode1.Decode.BitRate=100e+3 ' ", True)
scope.WriteString("""vbs 'app.SerialDecode.Decode1.Decode.ViewingMode="ASCII" ' """, True)
scope.WriteString("vbs 'app.SerialDecode.Decode1.Decode.InterframeTime=2e-3' ", True)
scope.WriteString("""vbs 'app.SerialDecode.Decode1.Decode.ByteOrderUI="LSB"' """, True)
scope.WriteString("""vbs 'app.SerialDecode.Decode1.Decode.PolarityUI="IdleHigh"' """, True)
scope.WriteString("vbs 'app.SerialDecode.Decode1.ViewDecode=1' ", True)

# Trigger on UART Pattern
#    - Serial Trigger
#    - UART
#    - C1
#    - 100 Kbps
#    - LSB
#    - IdleHigh
#    - Trigger on 3 DATA Equal 0x32 0x31 0x30 (ASCII = "210")
scope.WriteString("""vbs 'app.Acquisition.Trigger.TypeMainUI="Serial"' """, True)
scope.WriteString("""vbs 'app.Acquisition.Trigger.Type="UART"' """, True)
scope.WriteString("""vbs 'app.Acquisition.Trigger.Source="C1"' """, True)
scope.WriteString("vbs 'app.Acquisition.Trigger.Serial.UART.BitRate=100e+3 ' ", True)
scope.WriteString("""vbs 'app.Acquisition.Trigger.Serial.UART.ByteBitOrder="LSB"' """, True)
scope.WriteString("""vbs 'app.Acquisition.Trigger.Serial.UART.Polarity="IdleHigh"' """, True)
scope.WriteString("""vbs 'app.Acquisition.Trigger.Serial.UART.PatternOperator="Equal" ' """, True)
scope.WriteString("vbs 'app.Acquisition.Trigger.Serial.UART.PatternLength=3' ", True)
scope.WriteString("""vbs 'app.Acquisition.Trigger.Serial.UART.PatternValue="001100100011000100110000"' """, True)

scope.WriteString("""vbs 'app.Acquisition.TriggerMode="Single"' """, True)

# waiting loop
while True:
    scope.WriteString("vbs? 'Return = app.Acquisition.TriggerMode'", True)
    strVariable = scope.ReadString(20)
    if strVariable == "Stopped":
        break
for i in range(0, 16):
    str_i = str(i)
    scope.WriteString("vbs 'Cell = app.SerialDecode.Decode1.Out.Result.CellValue(1, 2) '", True)
    scope.WriteString("vbs? 'Return=Cell(0, "+str_i+")'", True)
    strVariable = scope.ReadString(50)
    dataFrame += strVariable
    
#Disconnects from the oscilloscope
scope.Disconnect()        
