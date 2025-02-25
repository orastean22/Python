# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Script Task: Search Burn in Serial no in all xlsx files with BI1 results
# -- Created on 24/02/2025
# -- Author: AdrianO
# -- Version 0.1 - Initial Version
# ----------------------------------------------------------------------------------------------
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Hardcoded serial number to search for
SEARCH_SERIAL_NUMBER = "H24320004K"

# Step 1: Select the folder where we have all xlsx files containing BI results
def search_serial_in_xlsx(folder_path, search_serial_number):
    files_found = []

    # List all Excel files in the directory
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file_name)

            try:
                # Load Excel file and read only first column (Serial Number)
                df = pd.read_excel(file_path, usecols=[0])  
                
                # Drop any empty rows to avoid NaN issues
                df.dropna(inplace=True)

                # Check if the serial number exists in column A (starting from A2)
                if search_serial_number in df.iloc[:, 0].values:
                    files_found.append(file_name)

            except Exception as e:
                print(f"Error reading {file_name}: {e}")

    return files_found

# Open a dialog to select the folder
root = tk.Tk()
root.withdraw()  # Hide the root window

folder_path = filedialog.askdirectory(title="Select Folder Containing Excel Files")
if not folder_path:
    print("No folder selected. Exiting...")
    exit()

# Call search function and perform the search
found_files = search_serial_in_xlsx(folder_path, SEARCH_SERIAL_NUMBER)

# Print results on terminal
if found_files:
    print("\nSerial number found in the following files:")
    for file in found_files:
        print(file)
else:
    print("\nSerial number not found in any files.")

# END 24.02.2025