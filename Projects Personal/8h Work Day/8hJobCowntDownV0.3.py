# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Script Task: Display 8h job countdown in digital format - real time in GUI
# -- Created on 08/01/2025
# -- Update on 
# -- Author: AdrianO
# -- Version 0.3 - Optimize the code
# ----------------------------------------------------------------------------------------------
import tkinter as tk

root = tk.Tk()
root.title("9-Hour Countdown")

remaining_seconds = 9 * 3600
clock_label = tk.Label(root, font=("Helvetica", 48), bg="black", fg="red")
clock_label.pack(anchor="center", fill="both", expand=True)

def format_time(seconds, extra=False):
    prefix = "+" if extra else ""
    hours, minutes = divmod(seconds, 3600)[0], (seconds % 3600) // 60
    return f"{prefix}{hours:02d}:{minutes:02d}:{seconds % 60:02d}"

def update_timer():
    global remaining_seconds, extra_seconds
    if remaining_seconds > 0:
        clock_label.config(text=format_time(remaining_seconds))
        remaining_seconds -= 1
    else:
        extra_seconds += 1
        clock_label.config(text=format_time(extra_seconds, extra=True), fg="green")
    clock_label.after(1000, update_timer)

extra_seconds = 0
update_timer()      # Start the countdown
root.mainloop()     # Start the GUI event loop

# END 04.02.2025 AdrianO