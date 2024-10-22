# userinterface.py
import tkinter as tk
from tkinter import messagebox
from percent import calculate_take_profit, calculate_stop_loss

class TradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Strategy Calculator")

        self.price_label = tk.Label(root, text="Enter Initial Price:")
        self.price_label.pack()

        self.price_entry = tk.Entry(root)
        self.price_entry.pack()

        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def calculate(self):
        try:
            price = float(self.price_entry.get())
            take_profit = calculate_take_profit(price)
            stop_loss = calculate_stop_loss(price)
            self.result_label.config(text=f"2% Take Profit: {take_profit}\n1% Stop Loss: {stop_loss}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value.")

def run_app():
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()