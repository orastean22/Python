# ------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 08/10/2024
# -- Update on 06/12/2024 - ONGOING
# -- Author: AdrianO
# -- Version 0.19 - Log in CSV file all P measurements +  temperature for oven
# --              - Auto start app button after 10 sec if the user do not start the app
# --              - Put Threshold detection by default on 33
# -- pip install pyvisa
# ------------------------------------------------------------------------------------------------------------------

import socket
import time
import csv
import os
import threading
import subprocess
import psutil
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import pyvisa as visa

# Initialize the VISA resource manager globally
rm = visa.ResourceManager()

# Global variable to control the data acquisition thread and LED status
running_event = threading.Event()
number_of_scopes = 2  # Default to 2 scopes
console_output_enabled = True  # Default to True (printing enable)
led_scope_1 = None
led_scope_2 = None

# Glitch counters for Scope 1 and Scope 2
glitch_count_scope_1 = 0
glitch_count_scope_2 = 0

# Variable that holds threshold value, default is 40.0 µs as pulse width
threshold_value = 33

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
        scope_1 = rm.open_resource("TCPIP0::10.30.11.31::inst0::INSTR")

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

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
            return True
    return False

def run_simserv_commands(path, port):
    simserv_exe = os.path.join(path, "simserv.exe")
    
    if not os.path.exists(simserv_exe):
        print(f"{simserv_exe} not found!")
        return

    if is_process_running("simserv.exe"):
        print("simserv.exe is already running. Skipping...")
        return
    
    try:
        simserv_process = subprocess.Popen([simserv_exe, "-D", f"-P{port}", "-start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("SimServ server started...")
        simserv_stdout, simserv_stderr = simserv_process.communicate(timeout=5)
        if simserv_stderr:
            print(f"SimServ error: {simserv_stderr}")
            return
        print(f"SimServ output: {simserv_stdout}")
    except subprocess.TimeoutExpired:
        print("A process took too long to respond.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("SimServ operations completed.")

# Function to read measurements from the scopes (P1 to P8)
def read_all_measurements_vbs_scope(scope, scope_name):
    try:
        # Initialize an empty list to store measurement values
        values_us = []

        # Query each P1 to P8 measurement individually
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
        if console_output_enabled:
            for i, value in enumerate(values_us, start=1):
                #if value < threshold_value:  # Check if the value is smaller than the threshold + display all in console
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

# Function that enable/disable console output
def toggle_console_output(toggle_button):
    global console_output_enabled
    
    # take the value from GUI
    console_output_enabled = not console_output_enabled  
    if console_output_enabled:
        toggle_button.config(text="Disable Console Output")
    else:
        toggle_button.config(text="Enable Console Output")

# Send a command to the oven and receive a response.
def send_command(ip, port, command):   
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            #print(f"Connected to {ip}:{port}")
            s.sendall(command.encode('latin-1'))  # Use 'latin-1' encoding for extended ASCII
            response = s.recv(1024)
            clean_response = response.decode('latin-1').strip()  # Strip unwanted characters
            #print(f"Response: {clean_response}")
            return clean_response
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_command_oven():
    oven_ip = "127.0.0.1"  
    oven_port = 7777  
    separator = chr(182)
    
    temperature_command = f"11004{separator}1{separator}1\r\n" 
    temp_response = send_command(oven_ip, oven_port, temperature_command)
    cleaned_response = temp_response[2:].strip()
    
    """# Log the result
    if temp_response:
        print(f"Temperature: {temp_response}")
    else:
        print(f"Failed to fetch temperature.")"""
    
    return cleaned_response

# Thread function to log data from Scope 1
def log_data_scope_1():
    global glitch_count_scope_1  # variable for use the global glitch counter for Scope 1
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
                temperature = send_command_oven()
                humidity = 0.0

                # Read all measurements from Scope 1 (P1 to P8 in one shot)
                measurement_scope_1 = read_all_measurements_vbs_scope(scope_1, "Scope_1_BOT_CH")

                # Log all measurements to CSV file only when below threshold
                for i, measurement in enumerate(measurement_scope_1, start=1):
                    if measurement != previous_measurements[i-1]:  # check if the value has changed
                        if measurement < threshold_value:  # Log values below threshold only
                            parameter = f"P{i}"
                            
                            # Increment glitch count for Scope 1 and update label
                            global glitch_count_scope_1
                            glitch_count_scope_1 += 1
                            detected_glitch_label_1.config(text=f"Detected Glitches Scope 1: {glitch_count_scope_1}")
                             
                            # Save to CSV after updating the counter
                            save_measurements_to_csv([timestamp, "Scope_1_BOT_CH", parameter, measurement, any_flag,
                                                  fault_a_flag, fault_b_flag, temperature, humidity], csv_filename)
                            previous_measurements[i-1] = measurement   # update previous measurement for next comparison
                            
    except Exception as e:
        print(f"Error in log_data_scope_1: {e}")
    finally:
        if scope_1:
            try:
                set_led_status(led_scope_1, "off")
                scope_1.close()  # Safely close the session
            except Exception as e:
                print(f"Error closing scope_1: {e}")
            # time.sleep(0.1)  # Delay between readings for updates every xxx mS
            # time.sleep(0.01)  # Read every 10ms (100 times per second)

# Thread function to log data from Scope 2
def log_data_scope_2():
    global glitch_count_scope_2  # variable for use the global glitch counter for Scope 1
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
                temperature = send_command_oven()
                humidity = 0.0

                # Read all measurements from Scope 2 (P1 to P8 in one shot)
                measurement_scope_2 = read_all_measurements_vbs_scope(scope_2, "Scope_2_TOP_CH")

                # Log all measurements to CSV file only when below threshold
                for i, measurement in enumerate(measurement_scope_2, start=1):
                    if measurement != previous_measurements[i - 1]:  # check if the value was change
                        if measurement < threshold_value:  # Log values below threshold only
                            parameter = f"P{i}"
                            
                            # Increment glitch count for Scope 1 and update label
                            global glitch_count_scope_2
                            glitch_count_scope_2 += 1
                            detected_glitch_label_2.config(text=f"Detected Glitches Scope 2: {glitch_count_scope_2}")
                            
                            # Save to CSV after updating the counter
                            save_measurements_to_csv(
                            [timestamp, "Scope_2_TOP_CH", parameter, measurement, any_flag, fault_a_flag, fault_b_flag,
                             temperature, humidity], csv_filename)
                            previous_measurements[i - 1] = measurement  # update previous measurement for next comparison
                            
    except Exception as e:
        print(f"Error in log_data_scope_2: {e}")

    finally:
        if scope_2:
            try:
                set_led_status(led_scope_2, "off")
                scope_2.close()  # Safely close the session
            except Exception as e:
                print(f"Error closing scope_2: {e}")
            # time.sleep(0.01)  # Read every 10ms (100 times per second)
 
def display_start_time(root):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time_label = tk.Label(root, text=f"App Start Time: {start_time}", font=("Arial", 10), anchor="e")
    start_time_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-30)  # Adjust x and y to position it
    return start_time

# Function to start data acquisition for one or both scopes in separate threads
def start_logging(start_button, threshold_entry, scope_selection, scope_1_radio, scope_2_radio):
    global threshold_value, number_of_scopes
    threshold_value = float(threshold_entry.get())  # Get threshold from the user entry GUI box

    if not running_event.is_set():
        running_event.set()
        start_button.config(state=tk.DISABLED)  # disable start button after starting
        number_of_scopes = scope_selection.get() # Get the selected number of scopes (1 or 2)
        
         # Disable unselected radio button
        if number_of_scopes == 1:
            scope_2_radio.config(state=tk.DISABLED)
        else:
            scope_1_radio.config(state=tk.DISABLED)
            
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
        time.sleep(0.1)  # Delay to allow final updates to be processed on GUI and CSV
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
    global led_scope_1, led_scope_2, detected_glitch_label_1, detected_glitch_label_2, glitch_count_scope_1, glitch_count_scope_2
    root = tk.Tk()
    root.title("Scope Data Logger")

    # Initialize glitch counts to 0
    glitch_count_scope_1 = 0
    glitch_count_scope_2 = 0
    
    # Set window size
    root.geometry("500x680")

    # Add title label on GUI
    label = tk.Label(root, text="Burin In 2 Monitoring", font=("Arial", 18, "bold"))
    label.pack(pady=20)

    # Add the app start time label
    display_start_time(root)  # Call the timer function here
    
    # Threshold input field with label
    threshold_label = tk.Label(root, text="Threshold (µs):", font=("Arial", 12))
    threshold_label.pack()
    threshold_entry = tk.Entry(root, font=("Arial", 12))
    threshold_entry.insert(0, "33.0")  # Default threshold value
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
                             command=lambda: start_logging(start_button, threshold_entry, scope_selection, scope_1_radio, scope_2_radio))
    start_button.pack(pady=10)

    # Stop button to stop data logging
    stop_button = tk.Button(root, text="Stop", font=("Arial", 14), command=stop_logging)
    stop_button.pack(pady=10)

    # Button to toggle console output
    toggle_button = tk.Button(root, text="Disable Console Output", font=("Arial", 14),command=lambda: toggle_console_output(toggle_button))
    toggle_button.pack(pady=10)

    # Exit button to close the GUI
    exit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=lambda: exit_program(root))
    exit_button.pack(pady=10)

    # LED indicators for Scope 1 and Scope 2
    led_scope_1 = tk.Label(root, text="Scope 1 Status", font=("Arial", 12), width=15, bg="grey")
    led_scope_1.pack(pady=10)
    led_scope_2 = tk.Label(root, text="Scope 2 Status", font=("Arial", 12), width=15, bg="grey")
    led_scope_2.pack(pady=10)

    # Labels for detected glitches in Scope 1 and Scope 2
    detected_glitch_label_1 = tk.Label(root, text="Glitch Detected on Scope_1: 0", font=("Arial", 12))
    detected_glitch_label_1.pack(pady=10)
    
    detected_glitch_label_2 = tk.Label(root, text="Glitch Detected on Scope_2: 0", font=("Arial", 12))
    detected_glitch_label_2.pack(pady=10)
    
    # Display Version on GUI
    version_label = tk.Label(root, text="V0.19 by AdrianO", font=("Arial", 10), anchor="se")
    version_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  # Position bottom-right
    
    # Automatically trigger the Start button after 10 seconds
    root.after(10000, lambda: start_logging(start_button, threshold_entry, scope_selection, scope_1_radio, scope_2_radio))

    root.mainloop()

# Main function to set up GUI
if __name__ == "__main__":
    run_simserv_commands("C:\\Simpati 4.80\\System", 7777)
    setup_gui()
    
# update 06.12.2024
# END
    
