# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 12/12/2024
# -- Update on 12/11/2024
# -- Author: AdrianO
# -- Script Task: Drow plot temperature based on csv file from Burn IN 2 Oven
# -- pip install pandas colorama
# -- clear terminal for WIN (os.system('cls')) and for MacOS/Linux (os.system('clear'))
# ----------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# Hide the root tkinter window
Tk().withdraw()

# Ask user to load a CSV file
file_path = filedialog.askopenfilename(title="Select a CSV file",filetypes=[("CSV files", "*.csv")])

if not file_path:
    print("No file selected. Please try again to select an CSV file..")
else:
    try:
        # Read the CSV file
        data = pd.read_csv(file_path)

        # Check for required columns
        if 'Data' not in data.columns or 'Timestamp' not in data.columns or 'Temperature' not in data.columns:
            raise ValueError("Required columns ('Data', 'Timestamp', 'Temperature') are missing from the CSV file.")
        
        # Display the first few rows of the dataset
        print("File loaded successfully. Preview here:")
        print(data.head())  # print only first few rows as head on terminal
    
        # Combine 'Data' and 'Timestamp' into a single column call datetime
        data['Timestamp'] = pd.to_datetime(data['Data'] + ' ' + data['Timestamp'])

        # Plot temperature vs. timestamp
        plt.figure(figsize=(10, 6))
        plt.plot(data['Timestamp'], data['Temperature'], marker='o', label='Temperature')

        # Customized the plot
        plt.title("Temperature vs. Time")
        plt.xlabel("Timestamp")
        plt.ylabel("Temperature (°C)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()

        # Show the plot
        plt.tight_layout()   # aligned titles without this option you can see overlapping titles
        plt.show()           # show the plot
    
    except ValueError as ve:
        print(f"Value Error: {ve}")    # if this error show up means ('Data', 'Timestamp', 'Temperature') are missing from the CSV file.
        
    except KeyError as ke:
        print(f"Key Error: Missing column in the CSV file - {ke}") # if this error show up means Key Error: Missing column in the CSV file - 'Temperature'
    
    except Exception as e:
        print("An error occurred while processing the CSV file.")
        print(f"Details: {e}")   # if this error show up the user will see An error occurred while processing the CSV file. Details: <description of the error>


        
        