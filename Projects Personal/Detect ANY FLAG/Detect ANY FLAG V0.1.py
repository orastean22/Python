# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 19/Sept/2024
# -- Author: AdrianO
# -- Version 0.1
# -- Script Task: Read one csv file and detect how many times we have ANY FLAG on TRUE - count them and display time
# -- stamp and temperature for each TRUE event
# ----------------------------------------------------------------------------------------------------------------------

import pandas as pd
from tkinter import Tk, filedialog


# Load the CSV file manually
# file_path = 'path_to_your_csv_file.csv'

# Function to open the file dialog and get the file path
def browse_file_and_check_csv():
    # Create a Tkinter root window (it will not be shown)
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a csv file ",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

# If the user didn't select a file, return None
    if not file_path:
        print("No file selected.")
        return None, False

# Check if the file has a .csv extension and try to load it
    if file_path.lower().endswith('.csv'):
        try:
            df = pd.read_csv(file_path, delimiter=';')
            print(f"The file {file_path} is a valid CSV file.")
            return file_path, True, df

        except Exception as e:
            print(f"Failed to read the file {file_path}. Error: {e}")
            return file_path, False, None

    else:
        print(f"The file {file_path} does not have a .csv extension.")
        return file_path, False, None


file_path, is_valid_csv, df = browse_file_and_check_csv()
if is_valid_csv:
    # Exclude the first row and filter for rows where 'Any flag' is True
    df_sliced = df.loc[1:]  # Exclude the first row
    true_events = df_sliced[df_sliced['Any flag'] == True]  # method counts TRUE values in the "Any flag" column.

    # Display the number of TRUE events
    true_count = true_events.shape[0]
    print("\n")  # Add one blank lines before displaying the result
    print(f"Number of TRUE events in 'Any flag' column (excluding the first row): {true_count}")

    # Display the Timestamp.abs and Temperature for each TRUE event
    for index, row in true_events.iterrows():
        print(f"Timestamp: {row['Timestamp.abs']}, Temperature: {row['Temperature']}")
else:
    print("The provided file is not a valid CSV.")
