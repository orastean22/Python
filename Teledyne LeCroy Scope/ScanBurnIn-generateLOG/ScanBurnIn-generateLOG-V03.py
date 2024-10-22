# Author: AdrianO
# Version V0.3 - update 16.09.2024
# Data: 23.08.2024
# to run the app go in Terminal cd /path/to/directory
# run the script: python3 ScanBurinIn-generateLOG.py
# Ver V0.3 solve the problem with swiss keyboard that change Z with Y (which is not good) we need to keep Z
# Scan serial numbers and generate a .txt file which includes the current date and time for each scanned unit.
# Trough error if we scann 2 or more times the same serial number
# open Termainal and install this:  pip install pywin32

import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import os
import ctypes
import win32api
import win32gui
import time

# Define the version number
version_number = "V0.3"

# Constants for the keyboard layouts
LANG_ENGLISH = 0x0409  # English (US)
LANG_SWISS = 0x0807    # Swiss (German)

# Function to set the keyboard layout for the current thread
def set_keyboard_layout(language_code):
    layout = ctypes.windll.user32.LoadKeyboardLayoutW(f"{language_code:04x}{language_code:04x}", 1)
    ctypes.windll.user32.ActivateKeyboardLayout(layout, 0)
    return layout

# Function to get the current keyboard layout
def get_current_keyboard_layout():
    hwnd = win32gui.GetForegroundWindow()  # Get the current window handle
    thread_id = win32api.GetCurrentThreadId()  # Get the current thread ID
    layout_id = ctypes.windll.user32.GetKeyboardLayout(thread_id)
    return layout_id

# Function to generate the batch file with scanned data
def generate_batch_file():
    try:
        # Ensure all serial numbers are filled
        if not all(entry.get().strip() for entry in serial_entries):
            messagebox.showerror("Error", "Please scan all 8 units before generating the file.")
            return

        # Check for duplicate serial numbers
        serial_numbers = [entry.get().strip().upper() for entry in serial_entries]    # Ensure uppercase
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
            batch_file_name = os.path.join(save_path, f"Batch {current_date}.txt")
        else:
            batch_file_name = os.path.join(desktop_path, f"Batch {current_date}.txt")

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
    serial_no = serial_entries[current_index].get().strip().upper()   # Convert to uppercase


    if serial_no:
        # Check for duplicates
        if serial_no in [serial_entries[i].get().strip().upper() for i in range(current_index)]:
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
root.title("Scan BI SN-V0.3")

# Set window size
root.geometry("265x410")  # Adjust the size to your preference

# Add version number label in the bottom-right corner
#version_label = tk.Label(root, text="Version V0.3", anchor="e")
#version_label.pack(side=tk.BOTTOM, anchor="se", padx=10, pady=5)

# Add instruction label
label_instruction = tk.Label(root, text="Scan the serial numbers of 8 units:")
label_instruction.pack(pady=10)

serial_entries = []

# Create 8 entry fields for 8 serial numbers
for i in range(8):
    frame = tk.Frame(root)
    frame.pack(pady=5)

    # Font for writings
    label = tk.Label(frame, text=f"Unit {i + 1}: ", font=("Helvetica", 9))
    label.pack(side=tk.LEFT, padx=10)

    entry = tk.Entry(frame, width=15)
    entry.pack(side=tk.LEFT)

    serial_entries.append(entry)

    # Bind the Return key to move to the next entry field and check for duplicates
    entry.bind('<Return>', lambda event, idx=i: scan_serial(event, idx))

# Function to handle exit and restore the original keyboard layout
def on_exit():
    # Restore the original keyboard layout
    set_keyboard_layout(original_layout)
    root.update()  # Force update of GUI events
    time.sleep(0.2)  # Add a small delay to ensure the layout changes
    root.quit()  # Close the app

# Button to generate the batch file
button_generate = tk.Button(root, text="Generate Batch File", command=generate_batch_file)
button_generate.pack(pady=20)

# Exit button to close the application and restore keyboard layout
button_exit = tk.Button(root, text="Exit", command=on_exit)
button_exit.pack(pady=10)

# Start the main event loop and set keyboard layout to English
def start_app():
    global original_layout
    original_layout = get_current_keyboard_layout()  # Get the original layout
    set_keyboard_layout(LANG_ENGLISH)  # Set to English layout

    # Ensure that the layout remains active during the program
    root.after(100, lambda: set_keyboard_layout(LANG_ENGLISH))

    # Start the GUI loop
    root.mainloop()

serial_entries[0].focus()  # Focus on the first entry field
start_app()


