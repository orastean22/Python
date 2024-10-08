# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 08/10/2024
# -- Author: AdrianO
# -- Version 0.4 - read all P1-P8 function on all 8 Channels on both scopes + create CSV file + GUI(include Start and
# Stop button for recording all events in CSV file + create 2 Threads (one for each scope) to read and log data in real
# time as possible. Add also two separate CSV files—one for each thread would simplify the process of real-time logging.
# Add also 0 in CSV file in case that one or more measurement points like P1...P8 do not nave value (no switching unit)
# -- Script Task: initiate scope for Burn IN 2 + read programs P1-P8 + create an CSV file.
# -- pip install pyvisa

import pyvisa as visa
import time
import csv
from datetime import datetime
import threading
import tkinter as tk
from tkinter import messagebox
import os

# Initialize the VISA resource manager globally
rm = visa.ResourceManager()

# Global variable to control the data acquisition thread
running = False

# Function to connect to Scope 1
def connect_to_oscilloscope_1():
    try:
        # Open connection to the oscilloscope using its IP address (or alias)
        scope_1 = rm.open_resource("TCPIP0::10.30.11.57::inst0::INSTR")
        scope_1.timeout = 5000  # Timeout set to 5 seconds
        print("\nYou are connected to the instrument Scope_1:\n", scope_1.query("*IDN?"))
        return scope_1
    except Exception as e:
        print(f"Failed to connect to oscilloscope_1: {e}")
        return None


# Function to connect to Scope 2
def connect_to_oscilloscope_2():
    try:
        # Open connection to the oscilloscope using its IP address (or alias)
        scope_2 = rm.open_resource("TCPIP0::10.30.11.43::inst0::INSTR")
        scope_2.timeout = 5000  # Timeout set to 5 seconds
        print("\nYou are connected to the instrument Scope_2:\n", scope_2.query("*IDN?"))
        return scope_2
    except Exception as e:
        print(f"Failed to connect to oscilloscope_2: {e}")
        return None

# Function to read measurements from the scopes
def read_measurement_vbs_scope(scope,parameter, scope_name):
    try:
        command = f"VBS? 'return=app.Measure.{parameter}.Out.Result.Value'"
        value_str = scope.query(command).replace('VBS ', '').strip()

        # Check if the result is "No Data Available"
        if "No Data Available" in value_str:
            print(f"{scope_name}_{parameter} Measurement: No Data Available")
            return 0 # Return 0 when no data is available
        else:
            # Convert the cleaned-up string to a float
            value = float(value_str)

            # Convert seconds to microseconds and round to 2 decimal
            value_us = round(value * 1_000_000,2)
            print(f"{scope_name}_{parameter} Measurement Value (in µs): {value_us:.2f} µs")
            return value_us

    except Exception as e:
        print(f"Error in VBS command: {e}")
        return 0 # Return 0 in case of any error

# Function to save measurements to CSV file
def save_measurements_to_csv(data, filename):
     with open(filename, mode='a', newline='') as file:
         writer = csv.writer(file, delimiter=';')
         writer.writerow(data)

# Function to write header to CSV file if it doesn't exist
def write_csv_header(filename):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            header = [
                'Timestamp', 'Scope', 'Parameter', 'Measurement (µs)',
                'Fault A Flag', 'Fault B Flag', 'Temperature', 'Humidity'
            ]
            writer.writerow(header)

# Thread function to log data from Scope 1
def log_data_scope_1():
    global running

    # CSV filename + today's data
    today_date = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"{today_date}_scope_1_measurements_BI_2.csv"

    # Write header if file doesn't exist
    write_csv_header(csv_filename)

    # Connect to scope 1
    scope_1 = connect_to_oscilloscope_1()

    if scope_1:
        while running:
            # Loop through P1 to P8 for Scope 1
            for i in range(1, 9):  # For P1 to P8
                parameter = f"P{i}"

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
            time.sleep(1)  # Small delay between readings

    # Close the scope connections after stopping
    scope_1.close()

# Thread function to log data from Scope 2
def log_data_scope_2():
    global running
    # CSV filename
    today_date = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"{today_date}_scope_2_measurements_BI_2.csv"

    # Write header if file doesn't exist
    write_csv_header(csv_filename)

    # Connect to Scope 2
    scope_2 = connect_to_oscilloscope_2()

    if scope_2:
        while running:
            # Loop through P1 to P8 for Scope 2
            for i in range(1, 9):
                parameter = f"P{i}"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fault_a_flag = 0
                fault_b_flag = 0
                temperature = 25.0
                humidity = 45.0

                # Read from Scope 2
                measurement_scope_2 = read_measurement_vbs_scope(scope_2, parameter, "Scope_2_TOP_CH")
                if measurement_scope_2 is not None:
                    save_measurements_to_csv(
                        [timestamp, "Scope_2_TOP_CH", parameter, measurement_scope_2, fault_a_flag, fault_b_flag, temperature, humidity],
                        csv_filename
                    )
            time.sleep(1)  # Small delay between readings

        # Close the scope connection after stopping
        scope_2.close()

        # Close the resource manager
        rm.close()

# Function to start the data acquisition for both scopes in separate threads
def start_logging():
    global running
    if not running:
       running = True
       # Start threads for both scopes
       thread_scope_1 = threading.Thread(target=log_data_scope_1)
       thread_scope_2 = threading.Thread(target=log_data_scope_2)
       thread_scope_1.start()
       thread_scope_2.start()
    else:
       messagebox.showinfo("Information", "Data logging is already running.")

# Function to stop the data acquisition
def stop_logging():
    global running
    if running:
       running = False
       messagebox.showinfo("Information", "Data logging stopped.")
    else:
       messagebox.showinfo("Information", "Data logging is not running.")

# Function to exit the program
def exit_program(root):
    global running
    if running:
        stop_logging()  # Ensure the logging is stopped before exiting
    root.quit()  # Close the GUI

# GUI setup
def setup_gui():
    root = tk.Tk()
    root.title("Scope Data Logger")

    # Start button
    start_button = tk.Button(root, text="Start", command=start_logging)
    start_button.pack(pady=10)

    # Stop button
    stop_button = tk.Button(root, text="Stop", command=stop_logging)
    stop_button.pack(pady=10)

    # Exit button
    exit_button = tk.Button(root, text="Exit", command=lambda: exit_program(root))
    exit_button.pack(pady=10)

    root.mainloop()

# Main function to set up GUI
if __name__ == "__main__":
    setup_gui()



