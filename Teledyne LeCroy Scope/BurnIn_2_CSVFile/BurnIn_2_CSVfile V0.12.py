# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 08/10/2024
# -- Author: AdrianO
# -- Version 0.12 - read all P1-P8 function for all 8 Channels on both scopes + create CSV file
# -- Script Task: initiate scope for Burn IN 2 + read programs P1-P8 + create an CSV file
# -- pip install pyvisa

import pyvisa as visa
import time
import csv
from datetime import datetime

# Initialize the VISA resource manager globally
rm = visa.ResourceManager()

def connect_to_oscilloscope_1():
    try:
        # Open connection to the oscilloscope using its IP address (or alias)
        scope_1 = rm.open_resource("TCPIP0::10.30.11.57::inst0::INSTR")
        scope_1.timeout = 5000  # Timeout set to 5 seconds (5000 milliseconds)
        print("\nYou are connected to the instrument Scope_1:\n", scope_1.query("*IDN?"))
        return scope_1
    except Exception as e:
        print(f"Failed to connect to oscilloscope_1: {e}")
        return None

def connect_to_oscilloscope_2():
    try:
        # Open connection to the oscilloscope using its IP address (or alias)
        scope_2 = rm.open_resource("TCPIP0::10.30.11.43::inst0::INSTR")
        scope_2.timeout = 5000  # Timeout set to 5 seconds (5000 milliseconds)
        print("\nYou are connected to the instrument Scope_2:\n", scope_2.query("*IDN?"))
        return scope_2
    except Exception as e:
        print(f"Failed to connect to oscilloscope_2: {e}")
        return None

def read_measurement_vbs_scope(scope,parameter, scope_name):
    try:
        # Dynamically build the VBS command for each parameter (P1, P2, ..., P8)
        command = f"VBS? 'return=app.Measure.{parameter}.Out.Result.Value'"
        value_str = scope.query(command)  # Read the VBS response as string

        # Strip out the 'VBS ' prefix and any trailing newline characters
        value_str = value_str.replace('VBS ', '').strip()

        # Check if the result is "No Data Available"
        if "No Data Available" in value_str:
            print(f"{scope_name}_{parameter} Measurement: No Data Available")
            return None
        else:
            # Convert the cleaned-up string to a float
            value = float(value_str)

            # Convert seconds to microseconds and round to 3 decimal
            value_us = round(value * 1_000_000,3)
            print(f"{scope_name}_{parameter} Measurement Value (in µs): {value_us:.3f} µs")
            return value_us

    except visa.VisaIOError as e:
        print(f"Visa IO Error in VBS: {e}")
        print("Check the VBS command or timeout settings.")
        return None
    except Exception as e:
        print(f"Error in VBS command: {e}")
        return None

def save_measurements_to_csv(data, filename):
    # Open the CSV file in append mode and write the data
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)

# Main function
def main():
    # CSV filename + today's data
    today_date = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"{today_date}_scope_measurements_BI_2.csv"

    # Write header to CSV (only once)
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        header = [
            'Timestamp', 'Scope', 'Parameter', 'Measurement (µs)',
            'Fault A Flag', 'Fault B Flag', 'Temperature', 'Humidity'
        ]
        writer.writerow(header)

    # Connect to both scopes
    scope_1 = connect_to_oscilloscope_1()
    scope_2 = connect_to_oscilloscope_2()
    if scope_1 and scope_2:
        # Loop through P1 to P8 for both scopes
        for i in range(1, 9):  # For P1 to P8
            parameter = f"P{i}"
            #   read_measurement_vbs_scope(scope_1, parameter, "Scope_1_Bottom_Channel")    # Read Px measurement value

            # Record the timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Add additional data (for example ....fault flags, temperature, humidity)
            fault_a_flag = 0
            fault_b_flag = 0
            temperature = 25.0
            humidity = 45.0

            # Read measurements from Scope 1
            measurement_scope_1 = read_measurement_vbs_scope(scope_1, parameter, "Scope_1_BOT_CH")
            if measurement_scope_1 is not None:
                save_measurements_to_csv(
                    [timestamp, "Scope_1_BOT_CH", parameter, measurement_scope_1, fault_a_flag, fault_b_flag, temperature,humidity],
                    csv_filename
                )

            # Read measurements from Scope 2
            measurement_scope_2 = read_measurement_vbs_scope(scope_2, parameter, "Scope_2_TOP_CH")
            if measurement_scope_2 is not None:
                save_measurements_to_csv(
                    [timestamp, "Scope_2_TOP_CH", parameter, measurement_scope_2, fault_a_flag, fault_b_flag, temperature,humidity],
                    csv_filename
                )

    # Close the Scope connection after reading the values
    if scope_1:
        scope_1.close()
    if scope_2:
        scope_2.close()

    # Close the resource manager
    rm.close()

if __name__ == "__main__":
    main()






