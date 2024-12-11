# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 22/10/2024
# -- Update on 28/10/2024
# -- Author: AdrianO
# -- Script Task: Load 16 JSON files and count read ll SO and bit stream errors.
# -- Version 0.1 - check and count SO and bit stream errors + display them
# -- pip install pandas colorama
# -- clear terminal for WIN (os.system('cls')) and for MacOS/Linux (os.system('clear'))
# ----------------------------------------------------------------------------------------------
import pandas as pd
from tkinter import Tk, filedialog
import os  # Import os for file path handling
import json  # Import json to read the JSON files
from colorama import Fore, Style, init  # Import colorama for coloring
import platform

from collections import defaultdict
from datetime import datetime

# Initialize colorama for colored text output
init(autoreset=True)

# Maps for units and their corresponding JSON files (ex: Dev1 and Dev2 for Unit 1....)
unit_json_mapping = {
    "Unit1": ["Dev1", "Dev2"],
    "Unit2": ["Dev3", "Dev4"],
    "Unit3": ["Dev5", "Dev6"],
    "Unit4": ["Dev7", "Dev8"],
    "Unit5": ["Dev9", "Dev10"],
    "Unit6": ["Dev11", "Dev12"],
    "Unit7": ["Dev13", "Dev14"],
    "Unit8": ["Dev15", "Dev16"]
}

# **********************************************************************************
# Select JSON files through a file dialog
# **********************************************************************************
def select_json_files():
    root = Tk()
    root.withdraw()  # Hide the root Tkinter window

    # Allow the user to select multiple JSON files
    file_paths = filedialog.askopenfilenames(
        title="Select JSON Files",
        filetypes=[("JSON files", "*.json")],
    )

    return list(file_paths)

# **********************************************************************************
# Function to count SO errors
# **********************************************************************************
def count_so_errors(error_entry):
    so_error_count = 0
    for error_line in error_entry.get("ErrorLines", []):
        if error_line.get("SO", "") == "Error":
            so_error_count += 1
    return so_error_count

# **********************************************************************************
# Function to count bitstream errors
# **********************************************************************************
def count_bitstream_errors(error_entry):
    bitstream_error_count = 0
    comment = error_entry.get("Comment", "")
    if comment.strip():  # Ensure we're not counting empty comments
        for line in comment.split("\r\n"):
            if line and line != "CRC_b21":  # Count each valid line as an error, excluding "CRC_b21"
                bitstream_error_count += 1
    return bitstream_error_count

# **********************************************************************************
# Reads JSON files and counts errors for each unit and device
# **********************************************************************************
def read_json_files(file_paths):

    unit_data = {f"Unit{i+1}": {} for i in range(8)}  # Create a dictionary for 8 units

    for file_path in file_paths:
        try:
             # Process each JSON file for errors
            current_file_errors, so_errors = process_json_data(file_path)
            
            # Correctly extract the JSON file name to identify Dev1, Dev2, etc.
            file_name = os.path.basename(file_path)  # Example: "SIC2192Log_tempDev1_..."
            dev_id = file_name.split("temp")[1].split('_')[0]  # Extract "DevX" part (Dev1, Dev2, etc.)

            # Identify and match device ID with units
            for unit, devices in unit_json_mapping.items():
                if dev_id in devices:
                    
                    # Count errors for the device in this unit
                    bitstream_error_count = sum(len(times) for times in current_file_errors.values())
                    so_error_count = len(so_errors)
                    
                            
                    # Store error counts for each device
                    unit_data[unit][dev_id] = {
                            'SO_errors': so_error_count,
                            'Bitstream_errors': bitstream_error_count
                        }
                    break  # Exit the loop once the unit is found for the device

        except Exception as e:
            print(f"Error reading {os.path.basename(file_path)}: {e}")

    return unit_data

# **********************************************************************************
# Combines date and time strings into a full datetime format.
# Returns a formatted string in "YYYY-MM-DD HH:MM:SS" format.
# ********************************************************************************** 
def format_full_time(date_str, time_str):
    try:
        # Combine the date (YYYY-MM-DD) and time (HH:MM:SS) with milliseconds
        full_datetime_str = f"{date_str} {time_str}"
        dt = datetime.strptime(full_datetime_str, "%Y-%m-%d %H:%M:%S.%f")  # Assuming milliseconds are present
        return dt.strftime("%Y-%m-%d %H:%M:%S")  # Return in "YYYY-MM-DD HH:MM:SS" format
    except ValueError:
        # If there's an error in parsing, return the original time string
        return full_datetime_str

# **********************************************************************************
# Extracts only the date part from the 'ErrTimeTick' field.
# **********************************************************************************
def extract_date_from_err_time_tick(err_time_tick):
    try:
        # Assuming "ErrTimeTick" is in "YYYY-MM-DD HH:MM:SS.fff" format, extract only the "YYYY-MM-DD" part
        date_only = err_time_tick.split()[0]  # Split by space and take the first part (date)
        return date_only
    except IndexError:
        # If there's an error in extracting the date, return the original string
        return err_time_tick

# **********************************************************************************
# Function to process a single JSON file, extracting and counting both SO and bitstream errors
# **********************************************************************************
def process_json_data(file_name):
    print(f"\n\033[1;34mProcessing JSON file: {file_name}\033[0m\n")

    with open(file_name, 'r') as file:
        data = json.load(file)

    # Dictionary to store the errors and corresponding times for the current JSON file
    current_file_errors = defaultdict(list)
    so_errors = []  # To store timestamps of SO errors

    # Iterate through the JSON data to extract "ErrTimeTick", "Comment", "SO", and "TimeChange"
    for error in data:
        err_time_tick = error.get("ErrTimeTick", "")  # Extract the ErrTimeTick field (date and time)
        date_only = extract_date_from_err_time_tick(err_time_tick)  # Extract only the date part (YYYY-MM-DD)

        # Process each line in "ErrorLines" for SO and bitstream errors
        for line in error.get("ErrorLines", []):
            comment = line.get("Comment", "")
            time_change = line.get("TimeChange", "")  # Extract the TimeChange field (time)
            so_error = line.get("SO", "")  # Check for "SO" error inside the ErrorLines

            # Count SO errors
            if so_error == "Error":
                full_datetime = format_full_time(date_only, time_change)
                so_errors.append(full_datetime)  # Store SO error timestamp

            # Count bitstream errors based on 'Comment' (exclude empty and "CRC_b21")
            if comment and comment != "CRC_b21":  # Ensure it's not empty and not "CRC_b21"
                full_datetime = format_full_time(date_only, time_change)
                # Split comment by lines and count each line as a separate bitstream error
                for bitstream_error in comment.split("\r\n"):
                    if bitstream_error:  # Ensure it's not an empty line
                        current_file_errors[bitstream_error].append(full_datetime)

    # Print if no errors are found
    if not current_file_errors and not so_errors:
        print(f"\n\033[1;32mNO error\033[0m\n")  # Green bold text for NO error
    else:
        # Display bitstream errors and timestamps
        for comment, times in current_file_errors.items():
            count = len(times)
            if count == 1:
                print(f"Error: {repr(comment)} occurred at {times[0]}")
            else:
                print(f"Error: {repr(comment)} occurred {count} time(s) at the following times:")
                for time in times:
                    print(f" - {time}")

    # Display SO errors
    if so_errors:
        print("\n\033[1;31mSO Errors Detected:\033[0m")  # Red text for SO errors
        so_count = len(so_errors)
        print(f"SO Error occurred {so_count} time(s) at the following times:")
        for so_error_time in so_errors:
            print(f" - {so_error_time}")

    return current_file_errors, so_errors  # Return both bitstream and SO errors


# **********************************************************************************
# Display error counts, highlighting units and devices with errors in red
# **********************************************************************************
def display_errors(unit_json_data):
    for unit, json_data in unit_json_data.items():
        
        # Check if the unit has errors, and display it in red if any errors are found
        unit_has_errors = any(count['SO_errors'] > 0 or count['Bitstream_errors'] > 0 for count in json_data.values())
        unit_display = f"{Fore.RED}{unit}" if unit_has_errors else unit
        print(f"\n{unit_display}")

        # Print the number of SO errors and Bitstream errors for each JSON file in the unit
        for json_file, counts in json_data.items():
            so_errors = counts['SO_errors']
            bitstream_errors = counts['Bitstream_errors']
            if so_errors > 0 or bitstream_errors > 0:
                print(f"{Fore.RED}{json_file}: {so_errors} SO errors, {bitstream_errors} Bitstream errors")
            else:
                print(f"{json_file}: {so_errors} SO errors, {bitstream_errors} Bitstream errors")
                
# **********************************************************************************
# Clears the terminal at the beginning of each run
# **********************************************************************************
def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system("clear")    

# **********************************************************************************
# Main process flow
# **********************************************************************************
def main():
    # Clear terminal function call
    clear_terminal()    
    
    # Step 1: Select the JSON files
    selected_json_files = select_json_files()

    if len(selected_json_files) == 16:  # Ensure exactly 16 JSON files are selected
        # Step 2: Read JSON data and map to units
        unit_json_data = read_json_files(selected_json_files)

        # Step 3: Display the SO error and bitstream error count for each JSON file
        display_errors(unit_json_data)

    else:
        print("Please select exactly 16 JSON files.")

if __name__ == "__main__":
    main()
    
# End - last update 28.10.2024 11:23AM