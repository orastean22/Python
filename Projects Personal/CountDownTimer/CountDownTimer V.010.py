# ------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 11/12/2024
# -- Update on 11/12/2024 - ONGOING
# -- Author: AdrianO
# -- Version 0.10 - Count down timer for Burn IN 2 
# --  
# ------------------------------------------------------------------------------------------------------------------

import tkinter as tk
from tkinter import font

def start_countdown():
    def countdown(count):
        if count >= 0:
            countdown_label.config(text=str(count), fg="red")
            root.after(1000, countdown, count - 1)
        else:
            countdown_label.config(text="Time's Up!", fg="red")

    countdown(time_var.get())

# Create the main window
root = tk.Tk()
root.title("Countdown Timer")
root.geometry("400x300")

# Set up the input and label
time_var = tk.IntVar()
time_var.set(10)  # Default countdown time in seconds

input_label = tk.Label(root, text="Enter countdown time (seconds):", font=("Arial", 12))
input_label.pack(pady=10)

input_entry = tk.Entry(root, textvariable=time_var, font=("Arial", 14), justify="center")
input_entry.pack(pady=10)

start_button = tk.Button(root, text="Start Countdown", command=start_countdown, font=("Arial", 14), bg="blue", fg="white")
start_button.pack(pady=20)

# Countdown label
countdown_label = tk.Label(root, text="", font=("Helvetica", 48, "bold"), fg="red")
countdown_label.pack(pady=20)

# Run the GUI
root.mainloop()
