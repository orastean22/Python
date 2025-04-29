import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_exe():
    # Request to select the main Python file (.py)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    py_file_path = filedialog.askopenfilename(
        title="Select Main Python File",
        filetypes=[("Python Files", "*.py")]
    )

    if not py_file_path:
        messagebox.showerror("Error", "No file selected.")
        return

    # Extract base filename without extension
    base_name = os.path.splitext(os.path.basename(py_file_path))[0]

    # Ask for output folder
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        messagebox.showerror("Error", "No output folder selected.")
        return

    # Check if PyInstaller is installed
    try:
        subprocess.run(['pyinstaller', '--version'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "PyInstaller is not installed. Please install it using 'pip install pyinstaller'.")
        return
    except FileNotFoundError:
        messagebox.showerror("Error", "PyInstaller is not found. Make sure it's installed and available in PATH.")
        return

    # Build the executable with PyInstaller
    try:
        subprocess.run([
            'pyinstaller',
            '--onefile',
            '--clean',
            '--name', base_name,
            '--distpath', output_folder,
            py_file_path
        ], check=True)
        messagebox.showinfo("Success", f"Executable '{base_name}.exe' created in:\n{output_folder}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Build Failed", f"PyInstaller failed:\n{e}")
    except Exception as ex:
        messagebox.showerror("Unexpected Error", str(ex))

if __name__ == "__main__":
    create_exe()