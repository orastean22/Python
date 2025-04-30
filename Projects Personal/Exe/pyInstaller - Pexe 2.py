import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import PyInstaller.__main__
import os
import threading
import sys
from datetime import datetime
import logging

class ExecutableCreator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Setup logging
        self.setup_logging()
        
        # Configure main window
        self.title("Python to EXE Converter")
        self.geometry("600x500")
        self.resizable(True, True)
        
        # Create main frame with padding
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Variables
        self.script_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.app_name = tk.StringVar()
        self.one_file = tk.BooleanVar(value=True)
        self.console_window = tk.BooleanVar(value=True)
        self.icon_path = tk.StringVar()
        
        # Set default output directory
        self.output_dir.set(os.path.join(os.path.expanduser("~"), "Desktop"))
        
        # Create GUI elements
        self.create_widgets(main_frame)
        
        # Status variables
        self.is_running = False
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"exe_creator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
    def create_widgets(self, parent):
        """Create all GUI widgets"""
        # Script selection
        script_frame = ttk.LabelFrame(parent, text="Script Selection", padding="5")
        script_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(script_frame, text="Python Script:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(script_frame, textvariable=self.script_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(script_frame, text="Browse", command=self.browse_script).grid(row=0, column=2)
        
        # Output directory
        output_frame = ttk.LabelFrame(parent, text="Output Settings", padding="5")
        output_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_output).grid(row=0, column=2)
        
        ttk.Label(output_frame, text="Application Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.app_name, width=50).grid(row=1, column=1, padx=5)
        
        # Options
        options_frame = ttk.LabelFrame(parent, text="Options", padding="5")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Checkbutton(options_frame, text="Create Single File", variable=self.one_file).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Show Console Window", variable=self.console_window).grid(row=0, column=1, sticky=tk.W)
        
        # Icon selection
        icon_frame = ttk.Frame(options_frame)
        icon_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(icon_frame, text="Icon File (optional):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(icon_frame, textvariable=self.icon_path, width=43).grid(row=0, column=1, padx=5)
        ttk.Button(icon_frame, text="Browse", command=self.browse_icon).grid(row=0, column=2)
        
        # Console output
        console_frame = ttk.LabelFrame(parent, text="Console Output", padding="5")
        console_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        parent.rowconfigure(3, weight=1)
        
        self.console = tk.Text(console_frame, height=10, width=50)
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(console_frame, orient=tk.VERTICAL, command=self.console.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.console['yscrollcommand'] = scrollbar.set
        
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        
        # Create button
        self.create_button = ttk.Button(parent, text="Create Executable", command=self.create_executable)
        self.create_button.grid(row=4, column=0, columnspan=2, pady=10)
        
    def browse_script(self):
        """Open file dialog to select Python script"""
        filename = filedialog.askopenfilename(
            title="Select Python Script",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if filename:
            self.script_path.set(filename)
            # Auto-set application name from script name
            suggested_name = os.path.splitext(os.path.basename(filename))[0]
            self.app_name.set(suggested_name)
    
    def browse_output(self):
        """Open directory dialog to select output location"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
    
    def browse_icon(self):
        """Open file dialog to select icon file"""
        filename = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[("Icon Files", "*.ico"), ("All Files", "*.*")]
        )
        if filename:
            self.icon_path.set(filename)
    
    def log_to_console(self, message):
        """Add message to console and log file"""
        self.console.insert(tk.END, f"{message}\n")
        self.console.see(tk.END)
        logging.info(message)
    
    def create_executable(self):
        """Create executable from selected Python script"""
        if self.is_running:
            messagebox.showwarning("Warning", "Process already running!")
            return
            
        if not self.script_path.get():
            messagebox.showerror("Error", "Please select a Python script!")
            return
            
        if not self.app_name.get():
            messagebox.showerror("Error", "Please enter an application name!")
            return
            
        # Disable button while running
        self.create_button.state(['disabled'])
        self.is_running = True
        
        # Clear console
        self.console.delete(1.0, tk.END)
        
        # Start process in separate thread
        thread = threading.Thread(target=self._create_executable_process)
        thread.start()
    
    def _create_executable_process(self):
        """Actual executable creation process"""
        try:
            self.log_to_console("Starting executable creation process...")
            
            # Build PyInstaller command
            command = ['--clean']  # Clean PyInstaller cache
            
            if self.one_file.get():
                command.append('--onefile')
            
            if not self.console_window.get():
                command.append('--noconsole')
            
            if self.icon_path.get():
                command.extend(['--icon', self.icon_path.get()])
            
            # Add name and output directory
            command.extend(['--name', self.app_name.get()])
            command.extend(['--distpath', self.output_dir.get()])
            
            # Add script path
            command.append(self.script_path.get())
            
            self.log_to_console("Running PyInstaller with following command:")
            self.log_to_console(" ".join(command))
            
            # Run PyInstaller
            PyInstaller.__main__.run(command)
            
            self.log_to_console("\nExecutable created successfully!")
            self.log_to_console(f"Output location: {self.output_dir.get()}")
            
            # Show success message
            messagebox.showinfo("Success", "Executable created successfully!")
            
        except Exception as e:
            error_msg = f"Error creating executable: {str(e)}"
            self.log_to_console(error_msg)
            messagebox.showerror("Error", error_msg)
            
        finally:
            # Re-enable button
            self.create_button.state(['!disabled'])
            self.is_running = False

def main():
    app = ExecutableCreator()
    app.mainloop()

if __name__ == "__main__":
    main()
