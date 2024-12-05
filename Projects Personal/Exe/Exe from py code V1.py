import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_exe():
    # Open a file dialog to select the Python file (.py)
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    py_file_path = filedialog.askopenfilename(
        title="Select Python file", filetypes=[("Python Files", "*.py")]
    )

    if not py_file_path:
        messagebox.showerror("Error", "No file selected")
        return

    # Check if PyInstaller is installed
    try:
        subprocess.check_call(['pyinstaller', '--version'])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", "PyInstaller is not installed. Please install it using 'pip install pyinstaller'.")
        return

    # Create the .exe using PyInstaller
    try:
        subprocess.check_call(['pyinstaller', '--onefile', py_file_path])
        messagebox.showinfo("Success", f"Executable created successfully for {os.path.basename(py_file_path)}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to create executable. Error: {str(e)}")

if __name__ == "__main__":
    create_exe()
