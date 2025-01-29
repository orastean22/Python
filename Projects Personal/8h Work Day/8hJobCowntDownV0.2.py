# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Script Task: Display 8h job countdown in digital format - real time in GUI
# -- Created on 08/01/2025
# -- Update on 
# -- Author: AdrianO
# -- Version 0.2 - Added additional green time increment after countdown
# ----------------------------------------------------------------------------------------------

import tkinter as tk
from datetime import datetime, timedelta
from time import strftime

root = tk.Tk()
root.title("9-Hour Countdown")

# Initial countdown time (9 hours in seconds)
remaining_seconds = 9 * 3600

# Define the clock label
clock_label = tk.Label(root, font=("Helvetica", 48), bg="black", fg="red")
clock_label.pack(anchor="center", fill="both", expand=True)

def update_extra_time():
    global extra_seconds
    extra_seconds += 1
    hours = extra_seconds // 3600
    minutes = (extra_seconds % 3600) // 60
    seconds = extra_seconds % 60
    time_string = f"+{hours:02d}:{minutes:02d}:{seconds:02d}"
    clock_label.config(text=time_string, fg="green")
    clock_label.after(1000, update_extra_time)

def update_countdown():
    global remaining_seconds
    if remaining_seconds > 0:
        hours = remaining_seconds // 3600
        minutes = (remaining_seconds % 3600) // 60
        seconds = remaining_seconds % 60
        
        time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        clock_label.config(text=time_string)
        remaining_seconds -= 1
        clock_label.after(1000, update_countdown)
    else:
        # Switch to green extra time
        global extra_seconds
        extra_seconds = 0
        time_string = f"+{extra_seconds//3600:02d}:{(extra_seconds%3600)//60:02d}:{extra_seconds%60:02d}"
        clock_label.config(text=time_string, fg="green")
        clock_label.after(1000, update_extra_time)

update_countdown()  # Start the countdown
root.mainloop()     # Start the GUI event loop

# END 29.01.2025 AdrianO

