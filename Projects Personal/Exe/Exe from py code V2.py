# build an exe file based on py file.

import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_exe():
    # Request to select the Python file (.py) in dialog box
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    py_file_path = filedialog.askopenfilename(
        title="Select Python file", filetypes=[("Python Files", "*.py")]
    )

    if not py_file_path:
        messagebox.showerror("Error", "No file selected")
        return

    # Open a directory dialog to select the output folder
    output_folder = filedialog.askdirectory(
        title="Select Output Folder"
    )

    if not output_folder:
        messagebox.showerror("Error", "No output folder selected")
        return

    # Check if PyInstaller is installed
    try:
        subprocess.check_call(['pyinstaller', '--version'])
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "PyInstaller is not installed. Please install it using 'pip install pyinstaller' in CMD.")
        return

    # Create the .exe using PyInstaller
    try:
        subprocess.check_call([
            'pyinstaller',
            '--onefile',
            '--distpath', output_folder,
            py_file_path
        ])
        messagebox.showinfo("Success", f"Executable created successfully at {output_folder}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to create executable. Error: {str(e)}")

if __name__ == "__main__":
    create_exe()
