#----------------------------------------------------------------------------------------------------------------------
#-- Python Script File
#-- Created on 05/Sept/2024
#-- Author: AdrianO
#-- Version 1.1
#-- Script Task:  Draw temperature graphic based on all errors from JSON file correlated with the time of BI events.
#-- Comment Vers 1.1: Integrate ExtractBitstreamErrorJSON_V3.py in basic code of
#-- pip install pandas
#----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import re  # for regular expression matching
from collections import defaultdict
from datetime import datetime

# Function to open the file dialog and get the file path
def browse_file(file_type, file_extension):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title=f"Select {file_type} file", filetypes=[(f"{file_type} files", file_extension)])
    return file_path

# Function to extract the serial number from the TXT file based on DUT type
def get_serial_number(txt_content, dut_type):
    pattern = rf"{dut_type}_(\w+)"  # e.g., "DUT1_" or "DUT2_"
    match = re.search(pattern, txt_content)
    if match:
        return match.group(1)  # Return the serial number like "A242700023"
    return None

# Function to extract DUT type dynamically from the CSV file name
def extract_dut_type(file_name):
    # Search for the pattern "DUT x" where x is a number
    match = re.search(r"DUT[ _]?(\d+)", file_name)
    if match:
        return f"DUT{match.group(1)}"  # e.g., DUT1, DUT2, DUT8
    return None

# Function to extract Dev type dynamically from the JSON file name
def extract_dev_from_json(file_name):
    # Search for the pattern "Devx" where x is a number
    match = re.search(r"Dev(\d+)", file_name)
    if match:
        return f"Dev{match.group(1)}"
    return None

# Function to show error in a popup
def show_error_popup(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Error", message)
    root.destroy()

# Function to combine the date from ErrTimeTick and time from TimeChange into "YYYY-MM-DD HH:MM:SS" format
def format_full_time(date_str, time_str):
    try:
        # Combine the date (YYYY-MM-DD) from ErrTimeTick and time (HH:MM:SS) from TimeChange
        full_datetime_str = f"{date_str} {time_str}"
        dt = datetime.strptime(full_datetime_str, "%Y-%m-%d %H:%M:%S.%f")  # Parse date and time, assuming milliseconds are present
        return dt.strftime("%Y-%m-%d %H:%M:%S")  # Return in "YYYY-MM-DD HH:MM:SS" format
    except ValueError:
        # If there's an error in parsing, return the original time string
        return f"{date_str} {time_str}"

# Function to extract only the date part from "ErrTimeTick"
def extract_date_from_err_time_tick(err_time_tick):
    try:
        # Assuming "ErrTimeTick" is in "YYYY-MM-DD HH:MM:SS.fff" format, extract only the "YYYY-MM-DD" part
        date_only = err_time_tick.split()[0]  # Split by space and take the first part (date)
        return date_only
    except IndexError:
        # If there's an error in extracting the date, return the original string
        return err_time_tick

# Function to load and display JSON errors
def process_json_data(file_name):
    print(f"\n\033[1;34mProcessing JSON file: {file_name}\033[0m\n")

    with open(file_name, 'r') as file:
        data = json.load(file)

    # Dictionary to store the errors and corresponding times for the current JSON file
    current_file_errors = defaultdict(list)

    # Iterate through the JSON data and extract "ErrTimeTick", "Comment", and "TimeChange" values
    for error in data:
        err_time_tick = error.get("ErrTimeTick", "")  # Extract the ErrTimeTick field (date and time)
        date_only = extract_date_from_err_time_tick(err_time_tick)  # Extract only the date part (YYYY-MM-DD)

        for line in error.get("ErrorLines", []):
            comment = line.get("Comment", "")
            time_change = line.get("TimeChange", "")  # Extract the TimeChange field (time)

            if comment and comment != "CRC_b21":  # Exclude CRC_b21
                # Combine the extracted date (YYYY-MM-DD) with the time from TimeChange
                full_datetime = format_full_time(date_only, time_change)
                current_file_errors[comment].append(full_datetime)
    # Check if there are no errors and print "NO error" if that's the case
    if not current_file_errors:
        print(f"\n\033[1;32mNO error\033[0m\n")  # Green bold text for NO error

    else:
            # Print out the errors and corresponding full timestamps for the current JSON file
            for comment, times in current_file_errors.items():
                count = len(times)
                if count == 1:
                    print(f"Error: {repr(comment)} occurred at {times[0]}")
                else:
                    print(f"Error: {repr(comment)} occurred {count} time(s) at the following times:")
                    for time in times:
                        print(f" - {time}")


# Function to load and validate the two JSON files
def load_json_files(dut_number):
    # Get the expected Dev numbers based on DUT number
    expected_dev1 = f"Dev{2 * dut_number - 1}"  # e.g., Dev1, Dev3, Dev5
    expected_dev2 = f"Dev{2 * dut_number}"  # e.g., Dev2, Dev4, Dev6

    # Load the JSON files dynamically based on the extracted Dev numbers
    json_file_path1 = browse_file(f"JSON file containing {expected_dev1}", "*.json")
    json_file_path2 = browse_file(f"JSON file containing {expected_dev2}", "*.json")

    # Extract the actual Dev numbers from the selected JSON files
    selected_dev1 = extract_dev_from_json(os.path.basename(json_file_path1))
    selected_dev2 = extract_dev_from_json(os.path.basename(json_file_path2))

    # Check if the selected files match the expected Dev files
    try:
        if selected_dev1 != expected_dev1:
            raise ValueError(f"Error: The first JSON file does not match the expected Dev file. Expected '{expected_dev1}', but got '{selected_dev1}'.")
        if selected_dev2 != expected_dev2:
            raise ValueError(f"Error: The second JSON file does not match the expected Dev file. Expected '{expected_dev2}', but got '{selected_dev2}'.")
    except ValueError as e:
        show_error_popup(str(e))  # Show error in a popup
        return None, None  # Return None if error occurred

    # Process and display the errors in both JSON files
    process_json_data(json_file_path1)
    process_json_data(json_file_path2)

    # Load the JSON data
    try:
        with open(json_file_path1, 'r') as json_file1:
            json_data1 = json.load(json_file1)

        with open(json_file_path2, 'r') as json_file2:
            json_data2 = json.load(json_file2)

        return json_data1, json_data2
    except json.JSONDecodeError as json_err:
        show_error_popup(f"Error while loading JSON: {json_err}")
        return None, None

# Load the CSV and TXT files using a file browser
csv_file_path = browse_file("CSV", "*.csv")
txt_file_path = browse_file("TXT", "*.txt")

# Extract the DUT type from the CSV filename
dut_type = extract_dut_type(os.path.basename(csv_file_path))

# Ensure that `dut_type` is properly extracted
if not dut_type:
    raise ValueError("DUT type could not be determined from the CSV filename.")

# Extract the DUT number from the DUT type
dut_number = int(dut_type.replace("DUT", ""))  # Convert DUT number to integer

# Load the JSON files for the given DUT number
json_data1, json_data2 = load_json_files(dut_number)

# If JSON loading was unsuccessful, exit
if json_data1 is None or json_data2 is None:
    exit()

# Continue with processing the files...
try:
    # Load the CSV file
    df = pd.read_csv(csv_file_path, delimiter=';')

    # Load the TXT file and read its content
    with open(txt_file_path, 'r') as txt_file:
        txt_content = txt_file.read()

    # Extract the serial number from the TXT file
    serial_number = None
    if dut_type:
        serial_number = get_serial_number(txt_content, dut_type)
        print(f"Serial number for {dut_type}: {serial_number}")
    else:
        print("No DUT number found in the CSV filename.")

    # Clean the 'Temperature' column: Replace values ending with 'm' by converting them to float properly
    df['Temperature'] = df['Temperature'].apply(lambda x: float(x.replace('m', '')) / 1000 if 'm' in str(x) else float(x))

    # Extract only the time part (HH:MM:SS) from the 'Timestamp.abs' column
    df['Time'] = pd.to_datetime(df['Timestamp.abs']).dt.strftime('%H:%M:%S')

    # Extract relevant columns for plotting
    time = df['Time']
    temperature = df['Temperature']

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(time, temperature, marker='o', linestyle='-', color='blue', label='Temperature Profile')

    # Create the main part of the title with red serial number
    if serial_number:
        plt.suptitle(f'Temperature Profile Over Time - {dut_type} Serial No: ', fontsize=12, color='black')
        plt.title(f'{serial_number}', fontsize=14, color='red', loc='center')
    else:
        plt.suptitle(f'Temperature Profile Over Time - {dut_type} Serial No: Not Found', fontsize=12)

    # Add labels for the plot
    plt.xlabel('Time (HH:MM:SS)')
    plt.ylabel('Temperature (°C)')

    # Rotate the time labels for better readability
    plt.xticks(rotation=45)

    # Add grid
    plt.grid(True)

    # Highlight specific temperatures (e.g., 75 and 64 degrees)
    special_temps = [75, 64]
    special_labels = ['Error 1', 'Error 2']

    # Find the closest times to these special temperatures (for simplicity, we'll just find the first occurrence)
    for i, temp in enumerate(special_temps):
        closest_index = (df['Temperature'] - temp).abs().idxmin()  # Get index of closest temperature
        closest_time = time[closest_index]
        closest_temp = temperature[closest_index]

        # Plot the big dot at the closest time and temperature - 'ro' for red circles
        plt.plot(closest_time, closest_temp, 'ro', markersize=12, label=special_labels[i])

        # Annotate the point with the error label
        plt.annotate(special_labels[i], (closest_time, closest_temp), textcoords="offset points", xytext=(0, 10), ha='center')

    # Show legend
    plt.legend()

    # Show the plot
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()

except pd.errors.EmptyDataError:
    print("Error: The file is empty.")
except pd.errors.ParserError:
    print("Error: The file could not be parsed. Check the file format.")
except json.JSONDecodeError as json_err:
    print(f"Error while loading JSON: {json_err}")
except Exception as e:
    print(f"An error occurred while processing the files: {e}")
