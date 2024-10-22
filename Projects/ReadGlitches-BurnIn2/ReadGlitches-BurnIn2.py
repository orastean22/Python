# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 22/10/2024
# -- Update on 22/10/2024 - not done yet
# -- Author: AdrianO
# -- Script Task: Read all P1 to P8 from CSV files(scope 1 + Scope 2)and how many glitches have one Batch run
# -- Version 0.1 - Load CVS files from Scope 1 and 2 + read and count P number
# --             - display in terminal how many glitches have each P number
# -- pip install pandas

import pandas as pd
from tkinter import Tk, filedialog


def select_csv_files():
    # Open a file dialog and select CSV files
    root = Tk()
    root.withdraw()  # Hide the root Tkinter window

    # Allow the user to select multiple files
    file_paths = filedialog.askopenfilenames(
        title="Select CSV Files",
        filetypes=[("CSV files", "*.csv")],
    )

    # Return selected file paths as a list
    return list(file_paths)


def read_csv_files(file_paths):
    # Create a list to store DataFrames
    dataframes = []

    # Iterate over each selected file and read them using pandas
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            dataframes.append(df)
            print(f"Successfully read file: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return dataframes


def main():
    # Step 1: Select the CSV files
    selected_files = select_csv_files()

    if len(selected_files) == 2:  # Ensure exactly 2 files are selected
        # Step 2: Read the CSV files
        dfs = read_csv_files(selected_files)

        # Example of processing or displaying the read DataFrames
        for i, df in enumerate(dfs):
            print(f"\nDataFrame {i + 1} Preview:\n")
            print(df.head())  # Print first 5 rows of each DataFrame
    else:
        print("Please select exactly 2 CSV files.")


if __name__ == "__main__":
    main()

