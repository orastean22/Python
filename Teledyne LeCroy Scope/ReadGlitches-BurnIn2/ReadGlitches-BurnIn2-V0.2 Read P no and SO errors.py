# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 21/10/2024
# -- Update on 22/10/2024
# -- Author: AdrianO
# -- Script Task: Read all P1 to P8 from CSV files(scope 1 + Scope 2) and count how many glitches (P1...P8) are found
# -- Version 0.1 - Load CSV files from Scope 1 and 2 + count and display occurrences of P1...P8 in 'PARAMETR' column
# -- Version 0.2 - read JSON files, check for SO errors, and highlight units with errors in red
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
# Open a file dialog and select CSV files
# **********************************************************************************
def select_csv_files():
    # The file paths of the selected files are returned as a list.
    root = Tk()
    root.withdraw()  # Hide the root Tkinter window

    # Allow the user to select multiple files
    file_paths = filedialog.askopenfilenames(
        title="Select CSV Files",
        filetypes=[("CSV files", "*.csv")],
    )

    # Return selected file paths as a list
    return list(file_paths)

# **********************************************************************************
# Reads the content of each CSV file into a DataFrame
# **********************************************************************************
def read_csv_files(file_paths):
    # Create a list to store DataFrames
    dataframes = []

    # Iterate over each selected file and read them using pandas
    for file_path in file_paths:
        try:
            # Try reading with utf-8 encoding first, and fall back to ISO-8859-1 if needed
            try:
                df = pd.read_csv(file_path, encoding='utf-8', delimiter=';')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')

            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {os.path.basename(file_path)}: {e}")

    return dataframes

# **********************************************************************************
# Counts occurrences of P1 to P8 in the 'Parameter' column of the DataFrame.
# **********************************************************************************
def count_p_parameters(df):
    # Initialize a dictionary to hold counts of P1...P8
    p_counts = {f'P{i}': 0 for i in range(1, 9)}

    # Check if the DataFrame contains the 'PARAMETR' column
    if 'Parameter' in df.columns:
        # Count occurrences of each P number (P1 to P8) in the 'Parameter' column
        for p in p_counts.keys():
            p_counts[p] = df['Parameter'].str.count(p).sum()

    return p_counts

# **********************************************************************************
# Selects JSON files and maps them to corresponding units.
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
# Reads the JSON files, checks for SO errors, and assigns them to corresponding units.
# **********************************************************************************
def read_json_files(file_paths):

    unit_data = {f"Unit{i+1}": {} for i in range(8)}  # Create a dictionary for 8 units

    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

                # Correctly extract the JSON file name to identify Dev1, Dev2, etc.
                file_name = os.path.basename(file_path)  # "SIC2192Log_tempDev1_..."
                dev_id = file_name.split("temp")[1].split('_')[0]  # Extract "DevX" part (Dev1, Dev2, etc.)

                # Match the extracted dev_id with the units
                for unit, devices in unit_json_mapping.items():
                    if dev_id in devices:
                        # Count the number of SO errors in this JSON file
                        so_error_count = 0
                        for error_entry in data:
                            for error_line in error_entry.get("ErrorLines", []):
                                if error_line.get("SO", "") == "Error":
                                    so_error_count += 1

                        # Store the SO error count for the current JSON file
                        unit_data[unit][dev_id] = so_error_count
                        break

        except Exception as e:
            print(f"Error reading {os.path.basename(file_path)}: {e}")

    return unit_data

# **********************************************************************************
# Main function that orchestrates the process:
# **********************************************************************************
def main():
    # Step 1: Select the CSV files
    selected_files = select_csv_files()

    if len(selected_files) == 2:  # Ensure exactly 2 files are selected
        # Step 2: Read the CSV files
        dfs = read_csv_files(selected_files)

        # Step 3: Count P1 to P8 in each DataFrame
        for i, df in enumerate(dfs):
            file_name = os.path.basename(selected_files[i])  # Get only the file name
            print(f"\n--- Results for file {file_name} ---")

            if df.empty:
                # If the DataFrame is empty, notify the user
                print(f"No data found in {file_name}.")
                continue

            # Step 4: Count occurrences of P1 to P8
            p_counts = count_p_parameters(df)

            # Check if all counts are zero (ex: no P1...P8 found)
            if all(count == 0 for count in p_counts.values()):
                print(f"No glitches found in {file_name}")
            else:
                # Display the counts, highlighting any glitches in red
                for p, count in p_counts.items():
                    if count > 0:
                        # Print in red if glitches are found
                        print(f"{Fore.RED}{p}: {count} occurrences")
                    else:
                        print(f"{p}: {count} occurrences")

        # Step 5: Select and read the JSON files
        selected_json_files = select_json_files()

        if len(selected_json_files) == 16:  # Ensure exactly 16 JSON files are selected
            # Read JSON data and map to units
            unit_json_data = read_json_files(selected_json_files)

            # Display the SO error count for each JSON file
            for unit, json_data in unit_json_data.items():
                # Check if the unit has errors, and display it in red if any errors are found
                unit_has_errors = any(count > 0 for count in json_data.values())
                unit_display = f"{Fore.RED}{unit}" if unit_has_errors else unit
                print(f"\n{unit_display}")

                # Print the number of SO errors for each JSON file in the unit
                for json_file, error_count in json_data.items():
                    if error_count > 0:
                        print(f"{Fore.RED}{json_file}: {error_count} SO errors")
                    else:
                        print(f"{json_file}: {error_count} SO errors")
        else:
            print("Please select exactly 16 JSON files.")

    else:
        # Notify the user if the wrong number of files is selected
        print("Please select exactly 2 CSV files.")


if __name__ == "__main__":
    main()

# END
# update 22.11.2024  18:00PM