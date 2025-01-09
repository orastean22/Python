# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Script Task: Display the actual clock in digital format - real time in GUI
# -- Created on 08/01/2025
# -- Update on 
# -- Author: AdrianO
# -- Version 0.1 - Digital Clock on GUI

# ----------------------------------------------------------------------------------------------

import tkinter as tk
from time import strftime

root = tk.Tk()
root.title("Digital Clock") # Display on GUI

# Define the clock label
clock_label = tk.Label(root,font=("Helvetica", 48), bg="black", fg="red")
clock_label.pack(anchor="center", fill="both", expand=True)

# Function to update the time
def update_time():
    current_time = strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time)

update_time()
root.mainloop()

#END 08.01.2024