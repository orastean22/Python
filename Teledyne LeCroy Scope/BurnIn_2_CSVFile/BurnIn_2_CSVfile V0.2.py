# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 08/10/2024
# -- Author: AdrianO
# -- Version 0.2 - read all P1-P8 function for all 8 Channels on both scopes
# -- Script Task: initiate scope for Burn IN 2 + read programs P1-P8 + create an CSV file
# -- pip install pyvisa

import pyvisa as visa
import time

# Initialize the VISA resource manager globally
rm = visa.ResourceManager()

def connect_to_oscilloscope_1():
    try:
        # Open connection to the oscilloscope using its IP address (or alias)
        scope_1 = rm.open_resource("TCPIP0::10.30.11.57::inst0::INSTR")
        scope_1.timeout = 5000  # Timeout set to 5 seconds (5000 milliseconds)
        print("\n You are connected to the instrument Scope_1:\n", scope_1.query("*IDN?"))
        return scope_1
    except Exception as e:
        print(f"Failed to connect to oscilloscope_1: {e}")
        return None

def connect_to_oscilloscope_2():
    try:
        # Open connection to the oscilloscope using its IP address (or alias)
        scope_2 = rm.open_resource("TCPIP0::10.30.11.43::inst0::INSTR")
        scope_2.timeout = 5000  # Timeout set to 5 seconds (5000 milliseconds)
        print("\n You are connected to the instrument Scope_2:\n", scope_2.query("*IDN?"))
        return scope_2
    except Exception as e:
        print(f"Failed to connect to oscilloscope_2: {e}")
        return None

def read_measurement_vbs_scope_1(scope_1,parameter):
    try:
        # Dynamically build the VBS command for each parameter (P1, P2, ..., P8)
        command = f"VBS? 'return=app.Measure.{parameter}.Out.Result.Value'"
        value_str = scope_1.query(command)  # Read the VBS response as string

        # Strip out the 'VBS ' prefix and any trailing newline characters
        value_str = value_str.replace('VBS ', '').strip()

        # Check if the result is "No Data Available"
        if "No Data Available" in value_str:
            print(f"Scope_1_Bottom_Channel_{parameter} Measurement: No Data Available")
        else:

            # Convert the cleaned-up string to a float
            value = float(value_str)

            # Convert seconds to microseconds
            value_us = value * 1_000_000
            print(f"Scope_1_Bottoom_Channel_{parameter} Measurement Value (in µs): {value_us:.6f} µs")

    except visa.VisaIOError as e:
        print(f"Visa IO Error in VBS: {e}")
        print("Check the VBS command or timeout settings.")
    except Exception as e:
        print(f"Error in VBS command: {e}")

def read_measurement_vbs_scope_2(scope_2,parameter):
    try:
        # Dynamically build the VBS command for each parameter (P1, P2, ..., P8)
        command = f"VBS? 'return=app.Measure.{parameter}.Out.Result.Value'"
        value_str = scope_2.query(command)  # Read the VBS response as string

        # Strip out the 'VBS ' prefix and any trailing newline characters
        value_str = value_str.replace('VBS ', '').strip()

        # Check if the result is "No Data Available"
        if "No Data Available" in value_str:
            print(f"Scope_1_Bottom_Channel_{parameter} Measurement: No Data Available")
        else:

            # Convert the cleaned-up string to a float
            value = float(value_str)

            # Convert seconds to microseconds
            value_us = value * 1_000_000
            print(f"Scope_2_TOP_Channel_{parameter} Measurement Value (in µs): {value_us:.6f} µs")

    except visa.VisaIOError as e:
        print(f"Visa IO Error in VBS: {e}")
        print("Check the VBS command or timeout settings.")
    except Exception as e:
        print(f"Error in VBS command: {e}")

# Main function
def main():
    scope_1 = connect_to_oscilloscope_1()  # Connect to Scope_1
    if scope_1:
        # Loop through P1 to P8 query values
        for i in range(1, 9):  # For P1 to P8
            parameter = f"P{i}"
            read_measurement_vbs_scope_1(scope_1, parameter)    # Read Px measurement value

    scope_2 = connect_to_oscilloscope_2()  # Connect to Scope_2
    if scope_2:
        # Loop through P1 to P8 query values
        for i in range(1, 9):  # For P1 to P8
            parameter = f"P{i}"
            read_measurement_vbs_scope_2(scope_2, parameter)  # Read Px measurement value






    # Close the Scope connection after reading the values
    scope_1.close()
    scope_2.close()

    # Close the resource manager
    rm.close()

if __name__ == "__main__":
    main()






