# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Script Task: Display 8h job countdown in digital format - real time in GUI
# -- Created on 08/01/2025
# -- Update on 
# -- Author: AdrianO
# -- Version 0.4 - Optimize the code introducing class
# --             - Positions window in top-right corner of screen
# --             - Uses Python's built-in timedelta for reliable time calculations
# ----------------------------------------------------------------------------------------------
import tkinter as tk
from datetime import datetime, timedelta

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("9-Hour Countdown")
        self.set_window_position()
        
        self.total_seconds = 10  # Initial 9-hour countdown
        self.is_overtime = False
        
        self.clock = tk.Label(root, font=("Helvetica", 48), bg="black", fg="red")
        self.clock.pack(anchor="ne")
        
        self.update_display()

    def set_window_position(self):
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"+{screen_width - 300}+20")

    def format_time(self, seconds):
        sign = "+" if self.is_overtime else ""
        return f"{sign}{timedelta(seconds=seconds)}"

    def update_display(self):
        if self.total_seconds >= 0 and not self.is_overtime:
            # Regular countdown phase
            time_str = str(timedelta(seconds=self.total_seconds))
            self.total_seconds -= 1
            color = "red"
        else:
            # Overtime phase
            self.is_overtime = True
            self.total_seconds += 1  # Counting up overtime
            time_str = f"+{timedelta(seconds=self.total_seconds)}"
            color = "green"

        self.clock.config(text=time_str, fg=color)
        self.root.after(1000, self.update_display)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()
    
# END 04.02.2025 AdrianO