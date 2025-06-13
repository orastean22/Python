# Trading Calculator for Buy/Sell Values
# This script creates a simple GUI application to calculate take profit and stop loss values based on a user input value.
# Author: AdrianO
# Date: 25 Mai 2025
# Version: 1.0
# Buy Sell Calculator with Take Profit and Stop Loss
#    Take Profit: 2% above the entry value
#    Stop Loss: 1% below the entry value
#    This is called a 2:1 risk/reward ratio
#***************************************************************************************************************************

import tkinter as tk
from tkinter import ttk

# Function to calculate take profit and stop loss based on user input and trade side
def calculate_values():
    try:
        entry_value = float(entry_value_input.get())   # Get the value entered by the user
        side = side_var.get() # Determine if it's a Buy or Sell
        # Calculation based on trade direction
        if side == "Buy":
            # For Buy: TP is 2% above entry, SL is 1% below entry
            take_profit = entry_value * 1.02
            stop_loss = entry_value * 0.99
        else:  # Sell
            # For Sell: TP is 2% below entry, SL is 1% above entry
            take_profit = entry_value * 0.98
            stop_loss = entry_value * 1.01
        
        # Display results in the GUI
        take_profit_label.config(text=f"Take Profit 2%: {take_profit:.2f}")
        stop_loss_label.config(text=f"Stop Loss 1%: {stop_loss:.2f}")
    except ValueError:
        # Handle invalid (non-numeric) input
        take_profit_label.config(text="Invalid input!")
        stop_loss_label.config(text="")

# --- GUI Setup ---

# Create main application window
root = tk.Tk()
root.title("Trading Calculator")

# Create and place the label and entry for the buy/sell value
ttk.Label(root, text="Enter Buy/Sell Value:").grid(row=0, column=0, padx=10, pady=10)
entry_value_input = ttk.Entry(root)
entry_value_input.grid(row=0, column=1, padx=10, pady=10)

# Dropdown to select Buy or Sell
side_var = tk.StringVar(value="Buy")
side_combo = ttk.Combobox(root, textvariable=side_var, values=["Buy", "Sell"], state="readonly", width=7)
side_combo.grid(row=0, column=2, padx=10, pady=10)

# Button to trigger the calculation
calculate_button = ttk.Button(root, text="Calculate", command=calculate_values)
calculate_button.grid(row=1, column=0, columnspan=3, pady=10)

# Labels to display the calculation results
take_profit_label = ttk.Label(root, text="TTake Profit 2%: ")
take_profit_label.grid(row=2, column=0, columnspan=3, pady=10)

stop_loss_label = ttk.Label(root, text="Stop Loss 1%: ")
stop_loss_label.grid(row=3, column=0, columnspan=3, pady=10)

# Start the main loop to show the GUI window
root.mainloop()

# END 13.06.2025































