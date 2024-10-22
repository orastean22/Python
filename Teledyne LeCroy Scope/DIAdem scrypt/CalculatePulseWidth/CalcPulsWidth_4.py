# --------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/22/2024 12:42:42
# -- Author: username
# -- Comment: .
# --------------------------------------------------------------------
import sys
if 'DIAdem' in sys.modules:
    from DIAdem import Application as dd

    if dd.AppEnableScriptDebugger:
        import debugpy
        debugpy.configure(python = sys.prefix + '\\python.exe')
        if not debugpy.is_client_connected():
            try:
                debugpy.listen(5678)
            except:
                pass
            debugpy.wait_for_client()

# --------------------------------------------------------------------
import math  # Import the math module for mathematical functions
# import clr
# clr.AddReference('NationalInstruments.DIAdem.API')
# from NationalInstruments.DIAdem.API import Data
# import win32com.client

# Connect to DIAdem
# diadem = win32com.client.Dispatch("Diadem.Application")

# Access Data object
# data = diadem.Data



# Define the function to calculate pulse width
def calculate_pulse_width(threshold):
    global signal_name  # Declare signal_name as global
    
    signal = Data.Root.ChannelGroups.Item(signal_name).Channels(1)
    signal_data = signal.Values
    sample_rate = signal.Properties("wfSampleRate").Value
    
    pulse_widths = []
    pulse_start = 0
    
    # Find pulse edges and calculate pulse widths
    for i in range(1, len(signal_data)):
        if signal_data[i] > threshold and signal_data[i - 1] <= threshold:
            pulse_start = i
        elif signal_data[i] <= threshold and signal_data[i - 1] > threshold and pulse_start > 0:
            pulse_end = i - 1
            # Calculate pulse width
            pulse_width = (pulse_end - pulse_start) / sample_rate
            pulse_widths.append(pulse_width)
            pulse_start = 0
    
    return pulse_widths

# Declare the name of your waveform signal
signal_name = "DUT1_Gate_B_Signal"

# Call the calculate_pulse_width function with the threshold
threshold = 100
pulse_widths = calculate_pulse_width(threshold)

# Print the calculated pulse widths
print("Pulse widths:", pulse_widths)


