# Author: AdrianO
# Version V0.1
# Data: 06.06.2024
# to run the app go in Terminal cd /path/to/directory
# run the script: python3 TimeCalculatorWithGUI.py

import tkinter as tk                        # For creating the GUI.
from tkinter import messagebox
from datetime import datetime, timedelta    # For time calculations.

def add_time(time_str, hours=0, minutes=0):
    original_time = datetime.strptime(time_str, '%H:%M')
    new_time = original_time + timedelta(hours=hours, minutes=minutes)
    return new_time.strftime('%H:%M')

def subtract_time(time_str, hours=0, minutes=0):
    original_time = datetime.strptime(time_str, '%H:%M')
    new_time = original_time - timedelta(hours=hours, minutes=minutes)
    return new_time.strftime('%H:%M')

def perform_operation():
    time_str = time_entry.get()
    operation = operation_var.get()
    try:
        hours = int(hours_entry.get())
        minutes = int(minutes_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for hours and minutes.")
        return

    if operation == 'add':
        new_time = add_time(time_str, hours, minutes)
    elif operation == 'subtract':
        new_time = subtract_time(time_str, hours, minutes)
    else:
        messagebox.showerror("Invalid operation", "Please select 'Add' or 'Subtract'.")
        return

    result_label.config(text=f"New time: {new_time}")

# Create the main window using tk.Tk()
root = tk.Tk()
root.title("Time Adder/Subtractor")
root.configure(bg='#f0f0f0')  # Background color Sets the background color of the main window to a light grey.

# Time input
tk.Label(root, text="Enter time (HH:MM):").grid(row=0, column=0, padx=10, pady=5)
time_entry = tk.Entry(root, bg='#ffffff', fg='#000000')   # bg='#ffffff' (white) and fg='#000000' (black)
time_entry.grid(row=0, column=1, padx=20, pady=5)

# Operation selection
operation_var = tk.StringVar(value="add")
tk.Label(root, text="Operation:", bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=5)
tk.Radiobutton(root, text="Add", variable=operation_var, value="add", bg='#f0f0f0').grid(row=1, column=1, padx=10, pady=5, sticky='w')
tk.Radiobutton(root, text="Subtract", variable=operation_var, value="subtract", bg='#f0f0f0').grid(row=1, column=1, padx=10, pady=5)

# Hours and minutes input
tk.Label(root, text="Hours:", bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=5)
hours_entry = tk.Entry(root, bg='#ffffff', fg='#000000')
hours_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Minutes:", bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=5)
minutes_entry = tk.Entry(root, bg='#ffffff', fg='#000000')
minutes_entry.grid(row=3, column=1, padx=10, pady=5)

# Perform operation button -  bg='#4caf50' (green) and fg='#ffffff' (white).
perform_button = tk.Button(root, text="Perform Operation", command=perform_operation, bg='#4caf50', fg='#ffffff')
perform_button.grid(row=4, columnspan=2, padx=10, pady=10)

# Result label
result_label = tk.Label(root, text="New time: ", bg='#f0f0f0', fg='#000000')
result_label.grid(row=5, columnspan=2, padx=10, pady=10)

# Start the main event loop
root.mainloop()   # Starts the Tkinter event loop to keep the window open.
