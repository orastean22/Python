# Author: AdrianO
# Version V0.1
# Data: 06.06.2024
# to run the app go in Terminal cd /path/to/directory
# run the script: python3 TimeCalculatorWithGUI.py

import tkinter as tk                        # For creating the GUI.
from tkinter import font
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

# Define colors
colors = {
    'red': '#f44336',
    'pink': '#e91e63',
    'purple': '#9c27b0',
    'deep_purple': '#673ab7',
    'indigo': '#3f51b5',
    'blue': '#2196f3',
    'light_blue': '#03a9f4',
    'cyan': '#00bcd4',
    'teal': '#009688',
    'green': '#4caf50',
    'light_green': '#8bc34a',
    'lime': '#cddc39',
    'yellow': '#ffeb3b',
    'amber': '#ffc107',
    'orange': '#ff9800',
    'deep_orange': '#ff5722',
    'brown': '#795548',
    'grey': '#9e9e9e',
    'blue_grey': '#607d8b',
    'black': '#000000',
    'white': '#ffffff'
}
#bg = colors['green']    # Green background
#fg = colors['white']    # White foreground

# Create the main window using tk.Tk()
root = tk.Tk()
root.title("Time Adder/Subtractor")
root.configure(bg = colors['black'])  # Background color of the main window

# Time input
tk.Label(root, text="Enter time (HH:MM):", bg = colors['black']).grid(row=0, column=0, padx=10, pady=5)
time_entry = tk.Entry(root, bg = colors['black'], fg = colors['white'])   # bg= (black) and fg=(white)
time_entry.grid(row=0, column=1, padx=20, pady=5)

# Operation selection
operation_var = tk.StringVar(value="add")
tk.Label(root, text="Operation:", bg = colors['black']).grid(row=1, column=0, padx=10, pady=5)
tk.Radiobutton(root, text="Add", variable=operation_var, value="add", bg = colors['black']).grid(row=1, column=1, padx=10, pady=5, sticky='w')
tk.Radiobutton(root, text="Subtract", variable=operation_var, value="subtract", bg = colors['black']).grid(row=1, column=1, padx=10, pady=5)

# Hours and minutes input
tk.Label(root, text="Hours:", bg = colors['black']).grid(row=2, column=0, padx=10, pady=5)
hours_entry = tk.Entry(root, bg = colors['black'], fg = colors['white'])
hours_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Minutes:", bg = colors['black']).grid(row=3, column=0, padx=10, pady=5)
minutes_entry = tk.Entry(root, bg = colors['black'], fg = colors['white'])
minutes_entry.grid(row=3, column=1, padx=10, pady=5)

# Create a custom font
custom_font = font.Font(family="Helvetica", size=12, weight="bold")

# Perform operation button
perform_button = tk.Button(
    root,
    text="Perform Operation",
    command=perform_operation,
    bg = colors['white'],   # Background color
    fg = colors['black'],   # Writing color
    font=custom_font,       # Apply custom font
    padx=20,                # Add padding inside the button
    pady=10,                # Add padding inside the button
    bd=5,                   # Add border width
    relief="raised",        # Use a raised relief style
    activebackground=colors['light_green'],    # Change background on click
    activeforeground=colors['black'])          # Change foreground on click
perform_button.grid(row=4, columnspan=2, padx=10, pady=10)

# Result label
result_label = tk.Label(root, text="New time: ", bg = colors['black'], fg = colors['red'])
result_label.grid(row=5, columnspan=2, padx=10, pady=10)

# Start the main event loop
root.mainloop()   # Starts the Tkinter event loop to keep the window open.
