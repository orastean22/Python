# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 08/10/2024
# -- Author: AdrianO
# -- Version 0.10 - read only P1 function
# -- Script Task: initiate scope for Burn IN 2 + read programs P1-P8 + create an CSV file
# -- pip install pyvisa

import pyvisa as visa
import time

# Initialize the VISA resource manager globally
rm = visa.ResourceManager()

def connect_to_oscilloscope():
    try:
        # Open connection to the oscilloscope using its IP address (or alias)
        scope = rm.open_resource("TCPIP0::10.30.11.57::inst0::INSTR")
        scope.timeout = 5000  # Timeout set to 5 seconds (5000 milliseconds)
        print("You are connected to the instrument:\n", scope.query("*IDN?"))
        return scope
    except Exception as e:
        print(f"Failed to connect to oscilloscope: {e}")
        return None

def read_p1_vbs_measurement(scope):
    try:
        # Test a VBS command to query pulse width statistics
        command = "VBS? 'return=app.Measure.P1.Out.Result.Value'"
        p1_value = (scope.query(command))

        # Strip out the 'VBS ' prefix and any trailing newline characters
        p1_value = p1_value.replace('VBS ', '').strip()

        # Convert the cleaned-up string to a float
        p1_value = float(p1_value)

        # Convert seconds to microseconds
        p1_value_us = p1_value * 1_000_000
        print(f"P1 Measurement Value (in µs): {p1_value_us:.6f} µs")
    except visa.VisaIOError as e:
        print(f"Visa IO Error in VBS: {e}")
        print("Check the VBS command or timeout settings.")
    except Exception as e:
        print(f"Error in VBS command: {e}")


# Main function
def main():
    scope = connect_to_oscilloscope()  # Connect to Scope
    if scope:
        read_p1_vbs_measurement(scope) # Read P1 measurement value
        scope.close()  # Close the Scope connection after reading the values
    rm.close()  # Close the resource manager

if __name__ == "__main__":
    main()






