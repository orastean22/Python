#----------------------------------------------------------------
#
# CEA TimeAtLevel Template
#
# 2024 V1.0
#
#----------------------------------------------------------------

#Import the library
import win32com.client # pywin32 for scope connection

#Create instance of the ActiveDSO control
scope = win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")

#connect to the oscilloscope, Substitute your IP address
scope.MakeConnection("IP:192.168.1.6")

#-----------------------
#TimeAtLevel measure P1
#50%
#positive slope
#------------------------
scope.WriteString("""vbs 'app.Measure.ViewP1="True" ' """, True)
scope.WriteString("""vbs 'app.Measure.P1.ParamEngine=TimeAtLevel" ' """, True)
scope.WriteString("""vbs 'app.Measure.P1.Operator.LevelType="Percent" ' """, True)
scope.WriteString("vbs 'app.Measure.P1.Operator.PercentLevel=50 ' ", True)
scope.WriteString("""vbs 'app.Measure.P1.Operator.Slope="Pos" ' """, True)

#read of P1
scope.WriteString("vbs? 'Return = app.Measure.P1.Out.Result.Value' ", True)
strVariable = scope.ReadString(20)

#Disconnects from the oscilloscope
scope.Disconnect()
