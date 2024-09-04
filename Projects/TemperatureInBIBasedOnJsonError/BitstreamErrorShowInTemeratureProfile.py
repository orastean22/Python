#----------------------------------------------------------------------------------------------------------------------
#-- Python Script File
#-- Created on 04/Sept/2024
#-- Author: AdrianO
#-- Comment: Draw temperature graphic based on all errors from JSON file correlated with the time of BI events.
#-- pip install pandas
#----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os

# File path with double backslashes
#file_path = 'C:/Python/Python/Projects/TemperatureInBIBasedOnJsonError/DATA/2024-09-03 09_34_50_000 SN  DUT 1.csv'
file_path = 'C:/Python/Python/Projects/TemperatureInBIBasedOnJsonError/DATA/2024-08-30 11_43_56_000 SN  DUT 2.csv'

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: The file '{file_path}' was not found.")
else:
    try:
        # Load the CSV file and read until delimiter
        df = pd.read_csv(file_path, delimiter=';')

        # Clean the 'Temperature' column: Replace values ending with 'm' by converting them to float properly ex:0.6 degree
        df['Temperature'] = df['Temperature'].apply(lambda x: float(x.replace('m', '')) / 1000 if 'm' in str(x) else float(x))

        # Extract only the time part (HH:MM:SS) from the 'Timestamp.abs' column (orig: 09:46:15.721 => extract 09:46:15)
        df['Time'] = pd.to_datetime(df['Timestamp.abs']).dt.strftime('%H:%M:%S')

        # Extract relevant columns for plotting
        time = df['Time']
        temperature = df['Temperature']

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(time, temperature, marker='o', linestyle='-', color='blue')
        

        # Add title and labels
        plt.title('Temperature Profile Over Time')
        plt.xlabel('Time (HH:MM:SS)')
        plt.ylabel('Temperature (°C)')

        # Rotate the time labels for better readability
        plt.xticks(rotation=45)

        # Add grid
        plt.grid(True)

        # Show the plot
        plt.tight_layout()  # Adjust layout to prevent clipping of labels
        plt.show()

    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file could not be parsed. Check the file format.")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
