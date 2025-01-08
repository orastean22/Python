# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Script Task: Display 8h job countdown in digital format - real time in GUI
# -- Created on 08/01/2025
# -- Update on 
# -- Author: AdrianO
# -- Version 0.1 - 8h Countdown Digital Clock on GUI
# ----------------------------------------------------------------------------------------------

import tkinter as tk
from datetime import datetime, timedelta
from time import strftime

root = tk.Tk()
root.title("9-Hour Countdown")

# Set the initial countdown time (9 hours in seconds) - Convert 9 hours to seconds (9 * 60 * 60 = 32400 seconds)
remaining_seconds = 9 * 3600

# Define the clock label
clock_label = tk.Label(root, font=("Helvetica", 48), bg="black", fg="red")
clock_label.pack(anchor="center", fill="both", expand=True)

# Function to update the countdown
def update_countdown():
    global remaining_seconds
    if remaining_seconds > 0:    # Check if countdown hasn't reached zero
        hours = remaining_seconds // 3600   # Calculate hours (integer division)
        minutes = (remaining_seconds % 3600) // 60    # Calculate minutes (remainder of hours, then divide)
        seconds = remaining_seconds % 60   # Calculate remaining seconds
        
        time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"    # Format time as HH:MM:SS with leading zeros
        clock_label.config(text=time_string)                        # Update the label with new time
        remaining_seconds -= 1                                      # Decrease remaining time by 1 second
        clock_label.after(1000, update_countdown)                   # Schedule next update in 1000ms (1 second)
    else:
        clock_label.config(text="00:00:00", fg="green")             # When countdown reaches zero, display 00:00:00

update_countdown()    # Start the countdown
root.mainloop()       # Start the main event loop of the application

# END 08.01.2025