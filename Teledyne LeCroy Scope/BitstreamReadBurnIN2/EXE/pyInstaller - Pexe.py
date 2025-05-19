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

        # Configurare tema intunecata
        self.configure(bg="#1e1e1e")
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.', background="#1e1e1e", foreground="white")
        style.configure('TLabel', background="#1e1e1e", foreground="white")
        style.configure('TButton', background="#3c3c3c", foreground="white")
        style.configure('TEntry', fieldbackground="#2e2e2e", foreground="white")
        style.configure('TCheckbutton', background="#1e1e1e", foreground="white")
        style.configure('TLabelframe', background="#1e1e1e", foreground="white")
        style.configure('TLabelframe.Label', background="#1e1e1e", foreground="white")

        self.title("Creare executabil din fișier Python...")
        self.geometry("530x500")
        self.resizable(True, True)
        #self.iconbitmap("C:/Windows/WinSxS/amd64_userexperience-shared_31bf3856ad364e35_10.0.26100.3323_none_b2c4fa5d70c6288d/UnplatedFolder.contrast-white.ico")

        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        self.script_path = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop"))
        self.app_name = tk.StringVar()
        self.one_file = tk.BooleanVar(value=True)
        self.console_window = tk.BooleanVar(value=True)
        self.icon_path = tk.StringVar()

        self.create_widgets(main_frame)
        self.setup_logging()
        self.is_running = False

    def setup_logging(self):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
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
        # Selectare script
        script_frame = ttk.LabelFrame(parent, text="Selectare Script", padding="5")
        script_frame.grid(row=0, column=0, sticky="ew", pady=5)
        script_frame.columnconfigure(1, weight=1)

        ttk.Label(script_frame, text="Script Python:").grid(row=0, column=0, sticky="w")
        ttk.Entry(script_frame, textvariable=self.script_path).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(script_frame, text="Browse", command=self.browse_script).grid(row=0, column=2)

        # Setări ieșire
        output_frame = ttk.LabelFrame(parent, text="Setări Ieșire", padding="5")
        output_frame.grid(row=1, column=0, sticky="ew", pady=5)
        output_frame.columnconfigure(1, weight=1)

        ttk.Label(output_frame, text="Director Ieșire:").grid(row=0, column=0, sticky="w")
        ttk.Entry(output_frame, textvariable=self.output_dir).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_output).grid(row=0, column=2)

        ttk.Label(output_frame, text="Nume Aplicație:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(output_frame, textvariable=self.app_name).grid(row=1, column=1, sticky="ew", padx=5)

        # Opțiuni
        options_frame = ttk.LabelFrame(parent, text="Opțiuni", padding="5")
        options_frame.grid(row=2, column=0, sticky="ew", pady=5)
        options_frame.columnconfigure(1, weight=1)

        ttk.Checkbutton(options_frame, text="Creează fișier unic", variable=self.one_file).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(options_frame, text="Afișează fereastră consolă", variable=self.console_window).grid(row=0, column=1, sticky="w")

        ttk.Label(options_frame, text="Fișier Icon (opțional):").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(options_frame, textvariable=self.icon_path).grid(row=1, column=1, sticky="ew", padx=5)
        ttk.Button(options_frame, text="Browse", command=self.browse_icon).grid(row=1, column=2)

        # Consolă
        console_frame = ttk.LabelFrame(parent, text="Ieșire Consolă", padding="5")
        console_frame.grid(row=3, column=0, sticky="nsew", pady=5)
        parent.rowconfigure(3, weight=1)
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)

        self.console = tk.Text(console_frame, height=10, bg="#2e2e2e", fg="white")
        self.console.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(console_frame, orient=tk.VERTICAL, command=self.console.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.console['yscrollcommand'] = scrollbar.set

        # Buton creare
        self.create_button = ttk.Button(parent, text="Creează Executabil", command=self.create_executable)
        self.create_button.grid(row=4, column=0, pady=10)

    def browse_script(self):
        filename = filedialog.askopenfilename(title="Selectează fișier Python", filetypes=[("Fișiere Python", "*.py")])
        if filename:
            self.script_path.set(filename)
            self.app_name.set(os.path.splitext(os.path.basename(filename))[0])

    def browse_output(self):
        directory = filedialog.askdirectory(title="Selectează director de ieșire")
        if directory:
            self.output_dir.set(directory)

    def browse_icon(self):
        filename = filedialog.askopenfilename(title="Selectează icon", filetypes=[("Fișiere ICO", "*.ico")])
        if filename:
            self.icon_path.set(filename)

    def log_to_console(self, message):
        self.console.insert(tk.END, f"{message}\n")
        self.console.see(tk.END)
        logging.info(message)

    def create_executable(self):
        if self.is_running:
            messagebox.showwarning("Avertisment", "Procesul rulează deja!")
            return

        if not self.script_path.get():
            messagebox.showerror("Eroare", "Selectează un fișier Python!")
            return

        if not self.app_name.get():
            messagebox.showerror("Eroare", "Introdu numele aplicației!")
            return

        self.create_button.state(['disabled'])
        self.is_running = True
        self.console.delete(1.0, tk.END)
        threading.Thread(target=self._create_executable_process).start()

    def _create_executable_process(self):
        try:
            self.log_to_console("Pornire proces creare executabil...")
            command = ['--clean']
            if self.one_file.get():
                command.append('--onefile')
            if not self.console_window.get():
                command.append('--noconsole')
            if self.icon_path.get():
                command.extend(['--icon', self.icon_path.get()])

            command.extend(['--name', self.app_name.get()])
            command.extend(['--distpath', self.output_dir.get()])
            command.append(self.script_path.get())

            self.log_to_console("Comandă PyInstaller:")
            self.log_to_console(" ".join(command))
            PyInstaller.__main__.run(command)

            self.log_to_console("\nExecutabil creat cu succes!")
            self.log_to_console(f"Locație: {self.output_dir.get()}")
            messagebox.showinfo("Succes", "Executabil creat cu succes!")

        except Exception as e:
            msg = f"Eroare la creare executabil: {str(e)}"
            self.log_to_console(msg)
            messagebox.showerror("Eroare", msg)

        finally:
            self.create_button.state(['!disabled'])
            self.is_running = False


def main():
    app = ExecutableCreator()
    app.mainloop()

if __name__ == "__main__":
    if "PYINSTALLER_SPLASH" not in os.environ:
        main()
