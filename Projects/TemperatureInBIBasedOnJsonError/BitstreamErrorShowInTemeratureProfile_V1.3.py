# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 05/Sept/2024
# -- Author: AdrianO
# -- Version 1.3  (09.09.2024)
# -- Script Task: Draw temperature graphic based on all errors from JSON file correlated with the time of BI events.
# -- Comment Vers 1.2: integrate all errors from Json bitstream only in plot
# -- Comment Vers 1.3: add also SO read out from all Json files and display on temperature graphic + add channels
# -- pip install pandas
# ----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # <--- Add this line
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import re  # for regular expression matching
from collections import defaultdict
from datetime import datetime
import textwrap  # For wrapping long legend labels


# Modify the plotting part where we add the legend labels for errors
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

# Function to load and display JSON errors, including SO errors
def process_json_data(file_name):
    print(f"\n\033[1;34mProcessing JSON file: {file_name}\033[0m\n")

    with open(file_name, 'r') as file:
        data = json.load(file)

    # Dictionary to store the errors and corresponding times for the current JSON file
    current_file_errors = defaultdict(list)
    so_errors = []  # To store SO errors

    # Iterate through the JSON data and extract "ErrTimeTick", "Comment", "SO", and "TimeChange" values
    for error in data:
        err_time_tick = error.get("ErrTimeTick", "")  # Extract the ErrTimeTick field (date and time)
        date_only = extract_date_from_err_time_tick(err_time_tick)  # Extract only the date part (YYYY-MM-DD)

        for line in error.get("ErrorLines", []):
            comment = line.get("Comment", "")
            time_change = line.get("TimeChange", "")  # Extract the TimeChange field (time)
            so_error = line.get("SO", "")  # Check for "SO" error inside the ErrorLines

            # If SO error is detected, store it with the corresponding timestamp
            if so_error =="Error":
                full_datetime = format_full_time(date_only, time_change)
                so_errors.append(full_datetime) # Store SO errors based on timestamp

            # Store the general errors
            if comment and comment != "CRC_b21":  # Exclude CRC_b21
                # Combine the extracted date (YYYY-MM-DD) with the time from TimeChange
                full_datetime = format_full_time(date_only, time_change)
                current_file_errors[comment].append(full_datetime)
    # Check if there are no errors and print "NO error" if that's the case
    if not current_file_errors and not so_errors:
       print(f"\n\033[1;32mNO error\033[0m\n")  # Green bold text for NO error

    else:
        # Print out the general errors and corresponding full timestamps for the current JSON file
        for comment, times in current_file_errors.items():
             count = len(times)
             if count == 1:
                 print(f"Error: {repr(comment)} occurred at {times[0]}")
             else:
                 print(f"Error: {repr(comment)} occurred {count} time(s) at the following times:")
                 for time in times:
                     print(f" - {time}")

    # Print out the SO errors for debugging
    if so_errors:
        print("\n\033[1;31mSO Errors Detected:\033[0m")  # Red text for SO errors
        so_count = len(so_errors)
        print(f"SO Error occurred {so_count} time(s) at the following times:")
        for so_error_time in so_errors:
            print(f" - {so_error_time}")

    return current_file_errors, so_errors  # Return both general errors and SO errors

# Function to determine if errors are in the Top Ch, Bottom Ch, or both
# Function to determine if errors are in the Top Ch, Bottom Ch, or both
def determine_channel(errors_json1, errors_json2, so_errors1, so_errors2):
    if (errors_json1 or so_errors1) and (errors_json2 or so_errors2):
        return "Top Ch and Bottom Ch"
    elif errors_json1 or so_errors1:
        return "Bottom Ch"
    elif errors_json2 or so_errors2:
        return "Top Ch"
    return None

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
        return None, None, None, None  # Return None if error occurred

    # Process and display the errors in both JSON files
    errors1, so_errors1 = process_json_data(json_file_path1)
    errors2, so_errors2 = process_json_data(json_file_path2)

    return errors1, errors2, so_errors1, so_errors2

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
errors_json1, errors_json2, so_errors1, so_errors2  = load_json_files(dut_number)

# If JSON loading was unsuccessful, exit
if errors_json1 is None or errors_json2 is None:
    exit()

# Determine if errors are on Top Ch, Bottom Ch, or both
channel_label = determine_channel(errors_json1, errors_json2, so_errors1, so_errors2)

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

    # Convert 'Timestamp.abs' to datetime objects for plotting and comparison
    df['Time'] = pd.to_datetime(df['Timestamp.abs'])

    # Extract relevant columns for plotting
    time = df['Time']
    temperature = df['Temperature']

    # Modify the plotting part of the code
    plt.figure(figsize=(15, 8), dpi=100)  # Increase figure size and resolution
    plt.plot(time, temperature, marker='o', linestyle='-', color='blue', label='Temperature Profile')

    # Create the main part of the title with red serial number and additional labels (Top Ch, Bottom Ch)
    if serial_number and channel_label:
        plt.suptitle(f'Temperature Profile Over Time - {dut_type} Serial No: ', fontsize=12)
        plt.title(f'{serial_number} | {channel_label}', fontsize=14, color='red', loc='center')
    elif serial_number:
        plt.suptitle(f'Temperature Profile Over Time - {dut_type} Serial No: ', fontsize=12)
        plt.title(f'{serial_number}', fontsize=14,color='red', loc='center')
    else:
        plt.suptitle(f'Temperature Profile Over Time - {dut_type} Serial No: Not Found | {channel_label}', fontsize=12)

    # Add labels for the plot
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')

    # Rotate the time labels for better readability
    plt.xticks(rotation=45)

    # Set date format for x-axis
    ax = plt.gca()  # Get the current axis
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # Automatically set date ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))  # Date format for better readability

    # Add grid
    plt.grid(True)

    # Combine all error times from both JSON files
    all_errors = defaultdict(list, {**errors_json1, **errors_json2})

    # Highlight errors with red dots and add legend labels for errors
    max_label_width = 50  # Maximum character width before wrapping
    for error, times in all_errors.items():
        # Wrap the error message into multiple lines
        wrapped_error = "\n".join(textwrap.wrap(f"{repr(error)} occurred {len(times)} time(s)", max_label_width))
        for i, error_time in enumerate(times):
            # Convert the full datetime string to a datetime object for matching with the plot
            error_time_obj = pd.to_datetime(error_time)
            closest_index = (time - error_time_obj).abs().idxmin()  # Get the index of the closest match
            # Plot the red dot for the error and include a label only for the first occurrence
            if i == 0:  # Only label the first dot to avoid clutter in the legend
                plt.plot(time[closest_index], temperature[closest_index], 'ro', markersize=12,label=wrapped_error)
            else:
                plt.plot(time[closest_index], temperature[closest_index], 'ro', markersize=12)  # Red dot without label for subsequent occurrences

    # Plot black dots for SO errors but add a single legend entry with the count of occurrences
    if so_errors1 or so_errors2:
        all_so_errors = so_errors1 + so_errors2  # Combine SO errors from both JSON files
        so_count = len(all_so_errors)

        # Plot SO errors as black dots without individual labels
        for so_error_time in all_so_errors:
            so_time_obj = pd.to_datetime(so_error_time)
            closest_index = (time - so_time_obj).abs().idxmin()  # Get the index of the closest match
            plt.plot(time[closest_index], temperature[closest_index], 'ko', markersize=8)  # Black dot for SO Error

        # Add a single legend entry for SO Error with the count of occurrences
        plt.plot([], [], 'ko', label=f"SO Error occurred {so_count} time(s)")

    # Modify the part of your code where the legend is shown
    plt.legend(loc='upper left')  # This will place the legend in the top-left corner of the plot

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

