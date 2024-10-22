# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 19/Sept/2024
# -- Author: AdrianO
# -- Version 0.2
# -- V0.1 => Script Task: Read one csv file and detect how many times we have ANY FLAG on TRUE -
# -- count them and display time stamp and temperature for each TRUE event
# -- V0.2 => draw a plot from -40 to +85 to display all TRUE events in ANY FLAG
# ----------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
from tkinter import Tk, filedialog
import matplotlib.pyplot as plt

# Load the CSV file manually
# file_path = 'path_to_your_csv_file.csv'


# Function to open the file dialog and get the file path
def browse_file_and_check_csv():
    # Create a Tkinter root window (it will not be shown)
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open the file dialog
    selected_file_path = filedialog.askopenfilename(
        title="Select a CSV file ",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

# Ensure the file is opened in read-only mode
    try:
           with open(selected_file_path, 'r') as file:
                dataframe = pd.read_csv(file, delimiter=';')
                print(f"The file {selected_file_path} is a valid CSV file.")
                return selected_file_path, True, dataframe

    except Exception as e:
        print(f"Failed to read the file {selected_file_path}. Error: {e}")
        return selected_file_path, False, None

file_path, is_valid_csv, dataframe = browse_file_and_check_csv()
if is_valid_csv:
    # Exclude the first row and filter for rows where 'Any flag' is True
    dataframe_sliced = dataframe.loc[1:]  # Exclude the first row
    true_events = dataframe_sliced[dataframe_sliced['Any flag']].copy()

    # Round the temperature to one decimal place for display and plotting
    true_events.loc[:, 'Temperature'] = true_events['Temperature'].round(1)

    # Display the number of TRUE events
    true_count = true_events.shape[0]
    print("\n")  # Add one blank lines before displaying the result
    print(f"Number of TRUE events in 'Any flag' column (excluding the first row): {true_count}")

    # Select first 10 and last 10 TRUE events if there are more than 20
    if true_count > 1000:
       first_10 = true_events.head(10)
       last_10 = true_events.tail(10)
       true_events_to_plot = pd.concat([first_10, last_10])
    else:
       true_events_to_plot = true_events

    # Display the selected TRUE events' details
    print("\nDetails of selected TRUE events:")
    for index, row in true_events_to_plot.iterrows():
      print(f"Timestamp: {row['Timestamp.abs']}, Temperature: {row['Temperature']}")

    # Plot the temperature values for the selected TRUE events
    plt.figure(figsize=(10, 6))
    plt.scatter(true_events_to_plot['Timestamp.abs'], true_events_to_plot['Temperature'], color='green', label='TRUE Events')
    plt.title('Temperature of Selected TRUE Events')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.ylim(-50, 100)  # Set temperature scale from -50°C to +100°C
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)

    # Add text annotation with total number of TRUE events in the top-left corner
    plt.text(-0.1, 1.05, f'Total TRUE Events: {true_count}', fontsize=12, ha='left', va='center',transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()  # Adjust layout to make room for the text
    plt.show()

else:
    print("The provided file is not a valid CSV.")
