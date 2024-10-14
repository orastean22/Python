# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 08/10/2024
# -- Author: AdrianO
# -- Version 0.5 - Add in CSV file ANY FLAG field
#                - Read much faster in mS like an active monitoring system
#                - Read all P1-P8 at the same time with updated read_all_measurements_vbs_scope method
#                - Include adjustable threshold for CSV logging in the GUI.
#                - add from GUI if we work with 1 or 2 scopes
# -- Script Task: Initialize scope for Burn IN 2 + read programs P1-P8 + create an CSV file.
# -- pip install pyvisa

import time
import csv
import os
import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import pyvisa as visa

# Initialize the VISA resource manager globally
rm = visa.ResourceManager()

# Global variable to control the data acquisition thread and LED status
running_event = threading.Event()
number_of_scopes = 2  # Default to 2 scopes
led_scope_1 = None
led_scope_2 = None

# Variable that holds threshold value, default is 40.0 µs as pulse width
threshold_value = 40.0

# Function to change LED status (green if the scopes are connected and reading values P1-P8)
def set_led_status(led, status):
    if status == "on":
        led.config(bg="green")
    else:
        led.config(bg="grey")

# Function to connect to Scope 1
def connect_to_oscilloscope_1():
    try:
        # Open connection to the oscilloscope using its IP address (or alias)
        scope_1 = rm.open_resource("TCPIP0::10.30.11.57::inst0::INSTR")

        # Timeout 5 sec -> timeout for communication with the scope;
        scope_1.timeout = 2000  # Program will wait for a response from the oscilloscope before raising an error

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
        scope_2.timeout = 2000  # Program will wait for a response from the oscilloscope before raising an error
        print("\nYou are connected to the instrument Scope_2:\n", scope_2.query("*IDN?"))
        return scope_2
    except Exception as e:
        print(f"Failed to connect to oscilloscope_2: {e}")
        return None

# Function to read measurements from the scopes (P1 to P8)
'''def read_measurement_vbs_scope(scope, parameter, scope_name):
    try:
        command = f"VBS? 'return=app.Measure.{parameter}.Out.Result.Value'"
        value_str = scope.query(command).replace('VBS ', '').strip()

        # Check if the result is "No Data Available"
        if "No Data Available" in value_str:
            print(f"{scope_name}_{parameter} Measurement: No Data Available")
            return 0   # Return 0 when no data is available
        else:
            # Convert the cleaned-up string to a float
            value = float(value_str)

            # Convert seconds to microseconds and round to 2 decimal
            value_us = round(value * 1_000_000, 4)
            print(f"{scope_name}_{parameter} Measurement Value (in µs): {value_us:.4f} µs")
            return value_us

    except Exception as e:
        print(f"Error in VBS command: {e}")
        return 0   # Return 0 in case of any error
'''

'''
def read_all_measurements_vbs_scope(scope, scope_name):
    try:
        # Initialize an empty list to store measurement values
        values_us = []

        # Query each P1 to P8 measurement individually in Python
        for i in range(1, 9):
            # VBS command to retrieve each measurement (P1 to P8)
            command = f"VBS? 'return=app.Measure.P{i}.Out.Result.Value'"

            # Query the oscilloscope for the current measurement
            value_str = scope.query(command).replace('VBS ', '').strip()

            # Check if the result is valid and convert it to float
            if "No Data Available" in value_str or value_str == "":
                values_us.append(0)  # Append 0 if no data available
            else:
                value_us = round(float(value_str) * 1_000_000, 6)  # Convert to uS
                values_us.append(value_us)

        # Print all measurements for this scope
        for i, value in enumerate(values_us, start=1):
            print(f"{scope_name}_P{i} Measurement Value (in µs): {value:.6f} µs")

        return values_us

    except Exception as e:
        print(f"Error in VBS command for {scope_name}: {e}")
        return [0] * 8  # Return a list of 0s if there's an error
'''

def read_all_measurements_vbs_scope(scope, scope_name):
    try:
        # Initialize an empty list to store measurement values
        values_us = []

        # Query each P1 to P8 measurement individually in Python
        for i in range(1, 9):
            # VBS command to retrieve each measurement (P1 to P8)
            command = f"VBS? 'return=app.Measure.P{i}.Out.Result.Value'"

            # Query the oscilloscope for the current measurement
            value_str = scope.query(command).replace('VBS ', '').strip()

            # Check if the result is valid and convert it to float
            if "No Data Available" in value_str or value_str == "":
                values_us.append(0)  # Append 0 if no data available
            else:
                value_us = round(float(value_str) * 1_000_000, 6)  # Convert to microseconds
                values_us.append(value_us)

        # Print all measurements for this scope
        for i, value in enumerate(values_us, start=1):
            if value < threshold_value:  # Check if the value is smaller than the threshold + display all in console
                    print(f"{scope_name}_P{i} Measurement Value (in µs): {value:.6f} µs")
        return values_us

    except Exception as e:
        print(f"Error in VBS command for {scope_name}: {e}")
        return [0] * 8  # Return a list of 0s if there's an error

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
            header = ['Timestamp', 'Scope', 'Parameter', 'Measurement (µs)', 'Any Flag', 'Fault A Flag',
                      'Fault B Flag', 'Temperature', 'Humidity']
            writer.writerow(header)

# Thread function to log data from Scope 1
def log_data_scope_1():
    scope_1 = None  # Initialize scope_1 variable
    previous_measurements = [None] * 8  # Init previous measurements to track changes for P1-P8
    try:
        # CSV filename + today's data
        today_date = datetime.now().strftime("%Y-%m-%d")
        csv_filename = f"{today_date}_scope_1_measurements_BI_2.csv"

        # Write header if file doesn't exist
        write_csv_header(csv_filename)

        # Connect to scope 1
        scope_1 = connect_to_oscilloscope_1()

        if scope_1:
            # Turn the LED on  for Scope 1
            set_led_status(led_scope_1, "on")

            while running_event.is_set():
                # Record the timestamp + milliseconds -> # [:-3] Truncate to get uS
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                # Add additional raw data (Ex: ....ANY FLAG, FAULT A FLAG, FAULT B FLAG, TEMPERATURE, HUMIDITY)
                any_flag = fault_a_flag = fault_b_flag = 0
                temperature = 25.0
                humidity = 45.0

                # Read all measurements from Scope 1 (P1 to P8 in one shot)
                measurement_scope_1 = read_all_measurements_vbs_scope(scope_1, "Scope_1_BOT_CH")

                # Log all measurements to CSV file only when below threshold
                for i, measurement in enumerate(measurement_scope_1, start=1):
                    if measurement != previous_measurements[i-1]:  # check if the value was change
                        if measurement > 0 and measurement < threshold_value:  # Log values below threshold only
                            parameter = f"P{i}"
                            save_measurements_to_csv([timestamp, "Scope_1_BOT_CH", parameter, measurement, any_flag,
                                                  fault_a_flag, fault_b_flag, temperature, humidity], csv_filename)
                            previous_measurements[i-1] = measurement   # update previous measurement for next comp
    except Exception as e:
        print(f"Error in log_data_scope_1: {e}")
    finally:
        if scope_1:
            try:
                set_led_status(led_scope_1, "off")
                scope_1.close()  # Safely close the session
            except Exception as e:
                print(f"Error closing scope_1: {e}")
            # time.sleep(0.1)  # Delay between readings for updates every 100 milliseconds (10 times per second)
            # time.sleep(0.01)  # Read every 10ms (100 times per second)

# Thread function to log data from Scope 2
def log_data_scope_2():
    scope_2 = None  # Initialize scope_2 variable
    previous_measurements = [None] * 8  # Init previous measurements to track changes for P1-P8
    try:
        # CSV filename
        today_date = datetime.now().strftime("%Y-%m-%d")
        csv_filename = f"{today_date}_scope_2_measurements_BI_2.csv"

        # Write header if file doesn't exist
        write_csv_header(csv_filename)

        # Connect to Scope 2
        scope_2 = connect_to_oscilloscope_2()

        if scope_2:
            # Turn the LED on  for Scope 2
            set_led_status(led_scope_2, "on")

            while running_event.is_set():
                # Record the timestamp + milliseconds -> # [:-3] Truncate to get uS
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                # Add additional raw data (Ex: ....ANY FLAG, FAULT A FLAG, FAULT B FLAG, TEMPERATURE, HUMIDITY)
                any_flag = fault_a_flag = fault_b_flag = 0
                temperature = 25.0
                humidity = 45.0

                # Read all measurements from Scope 2 (P1 to P8 in one shot)
                measurement_scope_2 = read_all_measurements_vbs_scope(scope_2, "Scope_2_TOP_CH")

                # Log all measurements to CSV file only when below threshold
                for i, measurement in enumerate(measurement_scope_2, start=1):
                    if measurement != previous_measurements[i - 1]:  # check if the value was change
                        if measurement > 0 and measurement < threshold_value:  # Log values below threshold only
                            parameter = f"P{i}"
                            save_measurements_to_csv(
                            [timestamp, "Scope_2_TOP_CH", parameter, measurement, any_flag, fault_a_flag, fault_b_flag,
                             temperature, humidity], csv_filename)
                            previous_measurements[i - 1] = measurement  # update previous measurement for next comp
    except Exception as e:
        print(f"Error in log_data_scope_2: {e}")

    finally:
        if scope_2:
            try:
                set_led_status(led_scope_2, "off")
                scope_2.close()  # Safely close the session
            except Exception as e:
                print(f"Error closing scope_2: {e}")
            # time.sleep(0.1)  # Delay between readings for updates every 100 milliseconds (10 times per second)
            # time.sleep(0.01)  # Read every 10ms (100 times per second)


# Function to start data acquisition for one or both scopes in separate threads
def start_logging(start_button, threshold_entry, scope_selection):
    global threshold_value, number_of_scopes
    threshold_value = float(threshold_entry.get())  # Get threshold from the user entry GUI box

    if not running_event.is_set():
        running_event.set()
        start_button.config(state=tk.DISABLED)  # disable start button after starting
        number_of_scopes = scope_selection.get() # Get the selected number of scopes (1 or 2)

        if not running_event.is_set():
            running_event.set()
            start_button.config(state=tk.DISABLED)  # Disable start button after starting
        
         # Start threads based on the number of scopes selected
        if number_of_scopes == 1:
            threading.Thread(target=log_data_scope_1).start()
        else:
            threading.Thread(target=log_data_scope_1).start()
            threading.Thread(target=log_data_scope_2).start()
            
    else:
        messagebox.showinfo("Information", "Data logging is already running.")


# Function to stop the data acquisition
def stop_logging():
    if running_event.is_set():
        running_event.clear()
        messagebox.showinfo("Information", "Data logging stopped.")
    else:
        messagebox.showinfo("Information", "Data logging is not running.")


# Function to exit the program
def exit_program(root):
    global rm
    if running_event.is_set():
        stop_logging()  # Ensure the logging is stopped before exiting
    try:
        rm.close()  # Close the resource manager
    except Exception as e:
        print(f"Error closing resource manager: {e}")
    root.quit()  # Close GUI

# GUI setup
def setup_gui():
    global led_scope_1, led_scope_2
    root = tk.Tk()
    root.title("Scope Data Logger")

    # Set window size
    root.geometry("400x500")

    # Add title label on GUI
    label = tk.Label(root, text="Burin In 2 Monitoring", font=("Arial", 18, "bold"))
    label.pack(pady=20)

    # Threshold input field with label
    threshold_label = tk.Label(root, text="Threshold (µs):", font=("Arial", 12))
    threshold_label.pack()
    threshold_entry = tk.Entry(root, font=("Arial", 12))
    threshold_entry.insert(0, "40.0")  # Default threshold value
    threshold_entry.pack(pady=5)
    
    # Scope selection label
    scope_label = tk.Label(root, text="Select number of scopes:", font=("Arial", 12))
    scope_label.pack() 
    
    # Frame for radio buttons
    scope_frame = tk.Frame(root)
    scope_frame.pack(pady=5)

    # Variable to store scope selection (1 or 2)
    scope_selection = tk.IntVar()
    scope_selection.set(2)  # Default to 2 scopes
     
    # Radio buttons for selecting 1 or 2 scopes 
    scope_1_radio = tk.Radiobutton(scope_frame, text="1 Scope", variable=scope_selection, value=1, font=("Arial", 12))
    scope_2_radio = tk.Radiobutton(scope_frame, text="2 Scopes", variable=scope_selection, value=2, font=("Arial", 12))
    scope_1_radio.pack(side="left", padx=5)
    scope_2_radio.pack(side="left", padx=5)

    # Start button to trigger data logging
    start_button = tk.Button(root, text="Start", font=("Arial", 14),
                             command=lambda: start_logging(start_button, threshold_entry, scope_selection))
    start_button.pack(pady=10)

    # Stop button to stop data logging
    stop_button = tk.Button(root, text="Stop", font=("Arial", 14), command=stop_logging)
    stop_button.pack(pady=10)

    # Exit button to close the GUI
    exit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=lambda: exit_program(root))
    exit_button.pack(pady=10)

    # LED indicators for Scope 1 and Scope 2
    led_scope_1 = tk.Label(root, text="Scope 1 Status", font=("Arial", 12), width=15, bg="grey")
    led_scope_1.pack(pady=10)
    led_scope_2 = tk.Label(root, text="Scope 2 Status", font=("Arial", 12), width=15, bg="grey")
    led_scope_2.pack(pady=10)

    # Display Version on GUI
    version_label = tk.Label(root, text="V0.5", font=("Arial", 10), anchor="se")
    version_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  # Position bottom-right

    root.mainloop()


# Main function to set up GUI


if __name__ == "__main__":
    setup_gui()
