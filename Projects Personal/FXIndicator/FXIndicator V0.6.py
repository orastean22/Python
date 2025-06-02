# Author: Adrian Orastean
# Date: 25 Mai 2025
# Description: Python script to create a simple indicator for financial data that fetches data from Yahoo Finance and plots it.
# offer you signal to buy or sell based on the custom strategy.
# Version: 0.6  - added GUI instead of Plot + setup an alarming system to notify you when a signal is generated
# pip install yfinance pandas matplotlib
# pip install python-binance

#----STRATEGY-----------------------------------------------------------------------------------------------------------------------------------
# BUY signal:  if BTC price rise > +3% in last 60 minutes
# SELL signal: if BTC price drop < -4% in last 60 minutes
#-----------------------------------------------------------------------------------------------------------------------------------------------
import os
import platform
from binance.client import Client
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import threading
import time

# --- Binance Setup (no API key needed) ---
client = Client()

first_reference_price = None

def generate_signal(change):
    if pd.isna(change):
        return None
    if change > 3:
        return 'BUY'
    elif change < -4:
        return 'SELL'
    else:
        return 'HOLD'

def play_alarm(signal_type):
    if platform.system() == "Windows":
        import winsound
        frequency = 1000 if signal_type == 'BUY' else 500
        duration = 700
        winsound.Beep(frequency, duration)
    else:
        # macOS / Linux - basic beep using system call
        sound_type = 'BUY' if signal_type == 'BUY' else 'SELL'
        os.system('say "{} signal"'.format(sound_type))

def get_initial_diff_text(current_price, first_ref_price):
    diff = ((current_price - first_ref_price) / first_ref_price) * 100
    color_code = '\033[94m'  # Blue
    reset_code = '\033[0m'
    return f"{color_code}{diff:.2f}%{reset_code}"

def create_gui():
    global root, tree
    root = tk.Tk()
    root.title("BTC Price Signals")
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt

    columns = ("Time", "Now_Price", "Ref_1h_Ago", "Price Change %", "Signal", "Initial Diff %")
    tree = ttk.Treeview(root, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill='both', expand=True)

    global fig, ax, canvas
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.set_title("BTC Binance Price with Buy/Sell Signals")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (USD)")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill='both', expand=True)

create_gui()

def update_data():
    global first_reference_price
    while True:
        klines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=120)

        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
        ])

        df['time'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Europe/Zurich')
        df.set_index('time', inplace=True)
        df['Binance_Close'] = df['close'].astype(float)
        df = df[['Binance_Close']]

        if first_reference_price is None:
            first_reference_price = df['Binance_Close'].shift(60).iloc[-1]
            blue = '\033[94m'
            reset = '\033[0m'
            up_3 = first_reference_price * 1.03
            down_4 = first_reference_price * 0.96
            green = '\033[92m'
            red = '\033[91m'
            print()
            print(f"{blue}Initial Ref Price (1h ago): {first_reference_price:.2f} "
                  f"{green}+3% Target: {up_3:.2f}{reset}  {red}-4% Target: {down_4:.2f}{reset}")
        
        # --- Apply Strategy: % Change Over Past 60 Minutes ---
        # Calculate the price change percentage over the last 60 minutes

        df['Price Change %'] = (df['Binance_Close'] - df['Binance_Close'].shift(60)) / df['Binance_Close'].shift(60) * 100
        reference_price = df['Binance_Close'].shift(60).iloc[-1]
        
        df['Signal'] = df['Price Change %'].apply(generate_signal)
        df['Price Change %'] = df['Price Change %'].round(2).astype(str) + '%'

        if 'header_printed' not in globals():
            bold = '\033[1m'
            reset = '\033[0m'
            print(f"{bold}{'Time':<25} {'Now_Price':<12} {'Ref_1h_Ago':<12} {'Price Change %':<15} {'Signal'}{reset}")
            global header_printed
            header_printed = True

        latest = df[['Binance_Close', 'Price Change %', 'Signal']].tail(1)
        row = latest.reset_index().iloc[0]
        change_value = float(row['Price Change %'].replace('%', ''))
        color_code = '\033[92m' if change_value >= 0 else '\033[91m'
        reset_code = '\033[0m'
        initial_diff_str = get_initial_diff_text(row['Binance_Close'], first_reference_price)
        print(f"{row['time'].strftime('%Y-%m-%d %H:%M'):<25} {row['Binance_Close']:<12.2f} {reference_price:<12.2f} {color_code}{row['Price Change %']:<15}{reset_code} {row['Signal']}  {initial_diff_str}")

        if row['Signal'] in ['BUY', 'SELL']:
            play_alarm(row['Signal'])

        gui_row = (row['time'].strftime('%Y-%m-%d %H:%M'), f"{row['Binance_Close']:.2f}", f"{reference_price:.2f}", row['Price Change %'], row['Signal'], initial_diff_str.strip('\033[94m\033[0m'))
        root.after(0, lambda r=gui_row: tree.insert('', 'end', values=r))

        ax.clear()
        ax.set_title("BTC Binance Price with Buy/Sell Signals")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price (USD)")
        ax.plot(df.index, df['Binance_Close'], color='orange', label='Binance BTC-USDT')

        buy_signals = df[df['Signal'] == 'BUY']
        sell_signals = df[df['Signal'] == 'SELL']
        ax.scatter(buy_signals.index, buy_signals['Binance_Close'], marker='^', color='green', label='BUY')
        ax.scatter(sell_signals.index, sell_signals['Binance_Close'], marker='v', color='red', label='SELL')

        ax.legend()
        canvas.draw()

        time.sleep(300)

# Run the updater in a thread and start the GUI
threading.Thread(target=update_data, daemon=True).start()
root.mainloop()

# END 01.06.2025. 