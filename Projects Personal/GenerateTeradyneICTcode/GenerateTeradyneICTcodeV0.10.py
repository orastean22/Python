# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 20/02/2025
# -- Author: AdrianO
# -- Version 0.10 - Draft version - read boom file.xlsx and extract designation + value in a new CSV file for next steps.
# -- Script Task: Generate ICT test program(all tpg files) based on boom file INPUT  
# --    Asic_Test.tpg; Capacitance_Test.tpg; Connector_Test.tpg; Diode_Test.tpg; Inductance_Test.tpg; Isolation_Test.tpg; Kontact_Test.tpg;
# --    Open_Test.tpg; Resistance_Test.tpg; Short_Test.tpg; Transformer_Test.tpg; Transistor_Test.tpg
# --    
# ----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import openpyxl
import tkinter as tk
from tkinter import filedialog

# Step 1: Select the BOM file using Open Dialog
root = tk.Tk()
root.withdraw()  # Hide the main window
file_path = filedialog.askopenfilename(title="Select BOM Excel File", filetypes=[("Excel Files", "*.xlsx")])

if not file_path:
    print("No file selected. Exiting.")
    exit()

# Step 2: Load workbook and select active sheet
wb = openpyxl.load_workbook(file_path, data_only=True)
sheet = wb.active

# Step 3: Manually set the starting positions for 'Value' and 'Designator'
value_col = 'C'  # Column C (starting at C9)
designator_col = 'D'  # Column D (starting at D9)
start_row = 9  # Row 9 is the first row with data

# Step 4: Extract data
output_csv_path = file_path.replace(".xlsx", "_extracted.csv")
with open(output_csv_path, "w", newline="") as csv_file:
    csv_writer = pd.DataFrame(columns=["Designator", "Value"])
    csv_writer.to_csv(csv_file, index=False)
    
    # Iterate through rows starting from row 9
    for row in sheet.iter_rows(min_row=start_row, values_only=True):
        value = str(row[2]).strip() if row[2] else ""
        designators = str(row[3]).strip().replace("\n", "").split(",") if row[3] else []
        
        for designator in designators:
            designator = designator.strip()
            if designator and value:
                new_row = pd.DataFrame([[designator, value]], columns=["Designator", "Value"])
                new_row.to_csv(csv_file, header=False, index=False)

print(f"Extracted BOM data saved to: {output_csv_path}")
