# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 21/10/2024
# -- Update on 22/10/2024
# -- Author: AdrianO
# -- Script Task: Read all P1 to P8 from CSV files(scope 1 + Scope 2) and count how many glitches (P1...P8) are found
# -- Version 0.1 - Load CSV files from Scope 1 and 2 + count and display occurrences of P1...P8 in 'PARAMETR' column
# -- pip install pandas colorama

import pandas as pd
from tkinter import Tk, filedialog
import os  # Import os for file path handling
from colorama import Fore, Style, init  # Import colorama for coloring

# Initialize colorama
init(autoreset=True)

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

            # Check if all counts are zero (i.e., no P1...P8 found)
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

    else:
        # Notify the user if the wrong number of files is selected
        print("Please select exactly 2 CSV files.")


if __name__ == "__main__":
    main()

# END
# update 22.11.2024  18:00PM
