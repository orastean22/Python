# Author: AdrianO
# Version V0.2
# Data: 23.08.2024
# to run the app go in Terminal cd /path/to/directory
# run the script: python3 ScanBurinIn-generateLOG.py

# Scan serial numbers and generate a .txt file which includes the current date and time for each scanned unit.
# Trough error if we scann 2 or more times the same serial number

import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import os

# Function to generate the batch file with scanned data
def generate_batch_file():
    try:
        # Ensure all serial numbers are filled
        if not all(entry.get().strip() for entry in serial_entries):
            messagebox.showerror("Error", "Please scan all 8 units before generating the file.")
            return

        # Check for duplicate serial numbers
        serial_numbers = [entry.get().strip() for entry in serial_entries]
        if len(serial_numbers) != len(set(serial_numbers)):
            messagebox.showerror("Error", "Duplicate serial numbers detected. Please enter unique serial numbers.")
            return

        # Get the current date for the filename
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")

        # Get the Desktop path for the current user
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

        # Check if the desktop exists
        if not os.path.exists(desktop_path):
            messagebox.showwarning("Warning", "Desktop folder not found. Please select a directory to save the file.")
            save_path = filedialog.askdirectory(title="Select Directory to Save the Batch File")
            if not save_path:
                return  # If the user cancels, exit the function
            batch_file_name = os.path.join(save_path, f"Batch_{current_date}.txt")
        else:
            batch_file_name = os.path.join(desktop_path, f"Batch_{current_date}.txt")

        # Open the file for writing
        with open(batch_file_name, 'w') as file:
            # Write data for each serial number scanned
            for i, serial_no in enumerate(serial_numbers, start=1):
                current_time = datetime.datetime.now().strftime("%d/%m/%Y;%I:%M:%S %p")
                file.write(f"{current_time};DUT{i}_{serial_no};BITSTREAMREADER_SN;ATVInterfaceBoard_SN;AdapterSlot_SN;\n\n")

        messagebox.showinfo("Success", f"Batch file '{batch_file_name}' created successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while generating the file: {e}")

# Function to handle serial number scanning and duplicate detection
def scan_serial(event, current_index):
    serial_no = serial_entries[current_index].get().strip()

    if serial_no:
        # Check for duplicates
        if serial_no in [serial_entries[i].get().strip() for i in range(current_index)]:
            messagebox.showerror("Error", "Duplicate serial number detected. Please enter a unique serial number.")
            serial_entries[current_index].delete(0, tk.END)
            serial_entries[current_index].focus()
        else:
            # Move to the next entry field
            if current_index < 7:
                serial_entries[current_index + 1].focus()
            else:
                messagebox.showinfo("Completed", "All 8 units scanned!")
    else:
        messagebox.showerror("Error", "Please enter a valid serial number.")

# Setup the GUI window
root = tk.Tk()
root.title("Scan BI SN")

# Set window size
root.geometry("250x500")  # Adjust the size to your preference

# Add instruction label
label_instruction = tk.Label(root, text="Scan the serial numbers of 8 units:")
label_instruction.pack(pady=10)

serial_entries = []

# Create 8 entry fields for 8 serial numbers
for i in range(8):
    frame = tk.Frame(root)
    frame.pack(pady=5)

    label = tk.Label(frame, text=f"Unit {i + 1}: ", font=("Helvetica", 9))
    label.pack(side=tk.LEFT, padx=10)

    entry = tk.Entry(frame, width=15)
    entry.pack(side=tk.LEFT)

    serial_entries.append(entry)

    # Bind the Return key to move to the next entry field and check for duplicates
    entry.bind('<Return>', lambda event, idx=i: scan_serial(event, idx))

# Button to generate the batch file
button_generate = tk.Button(root, text="Generate Batch File", command=generate_batch_file)
button_generate.pack(pady=20)

# Exit button to close the application
button_exit = tk.Button(root, text="Exit", command=root.quit)
button_exit.pack(pady=10)

# Start the main event loop
serial_entries[0].focus()  # Focus on the first entry field
root.mainloop()
