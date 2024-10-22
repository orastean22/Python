#----------------------------------------------------------------------------------------------------------------------
#-- Python Script File
#-- Created on 04/Sept/2024
#-- Author: AdrianO
#-- Version 1
#-- Comment: Draw temperature graphic based on all errors from JSON file correlated with the time of BI events.
#-- pip install pandas
#----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
import json
import re  # for regular expression matching

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

# Function to get the corresponding JSON filenames based on DUT number
def extract_dev_from_json(file_name):
    # Search for the pattern "Devx" where x is a number
    match = re.search(r"Dev(\d+)", file_name)
    if match:
        return f"Dev{match.group(1)}"
    return None

# Load the CSV and TXT files using a file browser
csv_file_path = browse_file("CSV", "*.csv")
txt_file_path = browse_file("TXT", "*.txt")

# Extract the DUT type from the CSV filename
dut_type = extract_dut_type(os.path.basename(csv_file_path))

# Ensure that `dut_type` is properly extracted
if not dut_type:
    raise ValueError("DUT type could not be determined from the CSV filename.")

# Get the expected Dev numbers based on DUT number
dut_number = int(dut_type.replace("DUT", ""))  # Convert DUT number to integer
expected_dev1 = f"Dev{2 * dut_number - 1}"  # e.g., Dev1, Dev3, Dev5
expected_dev2 = f"Dev{2 * dut_number}"  # e.g., Dev2, Dev4, Dev6

# Load the JSON files dynamically based on the extracted Dev numbers
json_file_path1 = browse_file(f"JSON file containing {expected_dev1}", "*.json")
json_file_path2 = browse_file(f"JSON file containing {expected_dev2}", "*.json")

# Extract the actual Dev numbers from the selected JSON files
selected_dev1 = extract_dev_from_json(os.path.basename(json_file_path1))
selected_dev2 = extract_dev_from_json(os.path.basename(json_file_path2))

# Check if the selected files match the expected Dev files
if selected_dev1 != expected_dev1:
    raise ValueError(f"Error: The first JSON file does not match the expected Dev file. Expected '{expected_dev1}', but got '{selected_dev1}'.")
if selected_dev2 != expected_dev2:
    raise ValueError(f"Error: The second JSON file does not match the expected Dev file. Expected '{expected_dev2}', but got '{selected_dev2}'.")

# Continue with processing the files...
print(f"Successfully loaded CSV with {dut_type}, JSON {selected_dev1}, and JSON {selected_dev2}")

# Load and process the files as in your previous code...
try:
    # Load the CSV file
    df = pd.read_csv(csv_file_path, delimiter=';')

    # Load the TXT file and read its content
    with open(txt_file_path, 'r') as txt_file:
        txt_content = txt_file.read()

    # Load the JSON files
    with open(json_file_path1, 'r') as json_file1:
        json_data1 = json.load(json_file1)

    with open(json_file_path2, 'r') as json_file2:
        json_data2 = json.load(json_file2)

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
