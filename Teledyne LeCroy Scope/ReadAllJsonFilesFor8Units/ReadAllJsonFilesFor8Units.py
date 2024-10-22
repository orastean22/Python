# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 22/10/2024
# -- Update on 22/10/2024   - not working yet
# -- Author: AdrianO
# -- Script Task: Load 16 JSON files and count read ll SO and bit stream errors.
# -- Version 0.1 - check and count SO errors and bit stream + display
# -- pip install pandas colorama

import pandas as pd
from tkinter import Tk, filedialog
import os  # Import os for file path handling
import json  # Import json to read the JSON files
from colorama import Fore, Style, init  # Import colorama for coloring

# Initialize colorama
init(autoreset=True)

# Maps for units and their corresponding JSON files (e.g., Dev1 and Dev2 for Unit 1)
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
# Select JSON files and map them to corresponding units.
# **********************************************************************************
def select_json_files():
    """
    Opens a file dialog to allow the user to select 16 JSON files.
    Returns:
        list: A list of file paths for the selected JSON files.
    """
    root = Tk()
    root.withdraw()  # Hide the root Tkinter window

    # Allow the user to select multiple JSON files
    file_paths = filedialog.askopenfilenames(
        title="Select JSON Files",
        filetypes=[("JSON files", "*.json")],
    )

    return list(file_paths)

# **********************************************************************************
# Reads the JSON files, checks for SO errors and bitstream errors, and assigns them to corresponding units.
# **********************************************************************************
def read_json_files(file_paths):
    """
    Reads the JSON files, checks for SO errors and bitstream errors, and tracks the counts.

    Args:
        file_paths (list): A list of file paths to read.
    
    Returns:
        dict: A dictionary with each unit's JSON data and SO + bitstream error counts.
    """
    unit_data = {f"Unit{i+1}": {} for i in range(8)}  # Create a dictionary for 8 units

    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

                # Correctly extract the JSON file name to identify Dev1, Dev2, etc.
                file_name = os.path.basename(file_path)  # Example: "SIC2192Log_tempDev1_..."
                dev_id = file_name.split("temp")[1].split('_')[0]  # Extract "DevX" part (Dev1, Dev2, etc.)

                # Match the extracted dev_id with the units
                for unit, devices in unit_json_mapping.items():
                    if dev_id in devices:
                        # Count the number of SO errors and bitstream errors in this JSON file
                        so_error_count = 0
                        bitstream_error_count = 0

                        for error_entry in data:
                            # Count SO errors
                            for error_line in error_entry.get("ErrorLines", []):
                                if error_line.get("SO", "") == "Error":
                                    so_error_count += 1
                            
                            # Count Bitstream errors based on non-empty 'Comment' field
                            comment = error_entry.get("Comment", "")
                            if comment:
                                bitstream_error_count += len(comment.split("\r\n"))  # Count each error listed

                        # Store the SO error and bitstream error count for the current JSON file
                        unit_data[unit][dev_id] = {
                            'SO_errors': so_error_count,
                            'Bitstream_errors': bitstream_error_count
                        }
                        break

        except Exception as e:
            print(f"Error reading {os.path.basename(file_path)}: {e}")

    return unit_data

# **********************************************************************************
# Main function to display SO errors and bitstream errors.
# **********************************************************************************
def display_errors(unit_json_data):
    """
    Displays the SO errors and bitstream errors for each unit and device.

    Args:
        unit_json_data (dict): Dictionary containing error counts for each unit and device.
    """
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
# Main process flow
# **********************************************************************************
def main():
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
    
# End - not working yet
