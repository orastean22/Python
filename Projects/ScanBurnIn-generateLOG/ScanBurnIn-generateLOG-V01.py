# Author: AdrianO
# Version V0.1
# Data: 23.08.2024
# to run the app go in Terminal cd /path/to/directory
# run the script: python3 ScanBurinIn-generateLOG.py

# Scan serial numbers and generate a .txt file which includes the current date and time for each scanned unit.
# After scanning 8 units, the file will be saved

import tkinter as tk
from tkinter import messagebox
import datetime

import tkinter as tk
from tkinter import messagebox
import datetime


# Function to generate the batch file with scanned data
def generate_batch_file():
    if all(entry.get() for entry in serial_entries):
        # Get the current date
        current_date = datetime.datetime.now().strftime("%d_%m_%Y")
        batch_file_name = f"Batch_{current_date}.txt"

        # Writing to the file
        with open(batch_file_name, 'w') as file:
            for i, entry in enumerate(serial_entries, start=1):
                serial_no = entry.get()
                current_time = datetime.datetime.now().strftime("%d/%m/%Y;%I:%M:%S %p")
                file.write(
                    f"{current_time};DUT{i}_{serial_no};BITSTREAMREADER_SN;ATVInterfaceBoard_SN;AdapterSlot_SN;\n\n")

        messagebox.showinfo("Success", f"Batch file '{batch_file_name}' created successfully!")
    else:
        messagebox.showerror("Error", "Please scan all 8 units before generating the file.")


# Function to focus on the next entry after a serial is entered
def move_to_next_entry(current_index):
    if current_index < 7:
        serial_entries[current_index + 1].focus()


# Function to scan serial number and move to the next position
def scan_serial(event, current_index):
    if serial_entries[current_index].get().strip():
        move_to_next_entry(current_index)
    else:
        messagebox.showerror("Error", "Please enter a valid serial number.")


# Setting up the GUI
root = tk.Tk()
root.title("Batch Scanner")

# Instruction label
label_instruction = tk.Label(root, text="Scan the serial numbers of 8 units:")
label_instruction.pack(pady=10)

serial_entries = []

# Create 8 entry fields for 8 serial numbers
for i in range(8):
    frame = tk.Frame(root)
    frame.pack(pady=5)

    label = tk.Label(frame, text=f"Unit {i + 1}: ", font=("Helvetica", 12))
    label.pack(side=tk.LEFT, padx=10)

    entry = tk.Entry(frame, width=30)
    entry.pack(side=tk.LEFT)

    serial_entries.append(entry)

    # Bind return key to move to the next entry
    entry.bind('<Return>', lambda event, idx=i: scan_serial(event, idx))

# Generate button
button_generate = tk.Button(root, text="Generate Batch File", command=generate_batch_file)
button_generate.pack(pady=20)

# Start the main loop
serial_entries[0].focus()  # Focus on the first entry field
root.mainloop()
