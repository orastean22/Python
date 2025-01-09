# Author: AdrianO
# Version V0.1
# Data: 27.08.2024
# to run the app go in Terminal cd /path/to/directory
# run the script: python3 8hWorkDay.py
# install 2 packages with below commands in terminal:
# pip install plyer
# pip install notification

import time
import tkinter as tk
from plyer import notification

# Duration of work in seconds (8 hours and 24 minutes = (8 * 60 * 60) + (24 * 60))
# WORK_DURATION = (8 * 60 * 60) + (24 * 60)  # 8 hours and 24 minutes in seconds(30240 sec)
WORK_DURATION = 10

def show_popup():
    # Create a simple popup window using tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    tk.messagebox.showinfo("Workday Over!", "It's time to go home!")
    root.destroy()

def notify_desktop():
    try:
        # Attempt to send a desktop notification
        notification.notify(
            title='Workday Complete',
            message='Your 8-hour and 24-minute workday is complete. Time to go home!',
            app_name='Work Timer',
            timeout=10
        )
    except NotImplementedError:
        # Fallback to tkinter popup if desktop notification fails
        print("Notification failed, falling back to popup.")
        show_popup()


def countdown_timer():
    print("Starting your 8-hour and 24-minute work timer...")

    # Start countdown
    time.sleep(WORK_DURATION)

    # Once time is up, show the notification or fallback
    notify_desktop()


if __name__ == "__main__":
    countdown_timer()

#END  
