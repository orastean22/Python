# Author: Adrian Orastean
# Date: 25 Mai 2025
# Description: Python script to create a simple indicator for financial data that fetches data from Yahoo Finance and plots it.
# offer you signal to buy or sell based on the custom strategy.
# Version: 0.5  - added formatted % output and verified real-time strategy logic.
# pip install yfinance pandas matplotlib
# pip install python-binance

#----STRATEGY-----------------------------------------------------------------------------------------------------------------------------------
# BUY signal:  if BTC price rise > +3% in last 60 minutes
# SELL signal: if BTC price drop < -4% in last 60 minutes
#-----------------------------------------------------------------------------------------------------------------------------------------------
from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Enable interactive mode
plt.ion()  

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

def get_initial_diff_text(current_price, first_ref_price):
    diff = ((current_price - first_ref_price) / first_ref_price) * 100
    color_code = '\033[94m'  # Blue
    reset_code = '\033[0m'
    return f"{color_code}{diff:.2f}%{reset_code}"

while True:
    # Get recent 1-minute candles for last 2 hours
    klines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=120)

    # Convert to DataFrame
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
    ])

    # Format time & price
    df['time'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Europe/Zurich')
    df.set_index('time', inplace=True)
    df['Binance_Close'] = df['close'].astype(float)
    df = df[['Binance_Close']]

    if first_reference_price is None:
        first_reference_price = df['Binance_Close'].shift(60).iloc[-1]
        blue = '\033[94m'
        reset = '\033[0m'
        print(f"{blue}Initial Ref Price (1h ago): {first_reference_price:.2f}{reset}")

    # --- Apply Strategy: % Change Over Past 60 Minutes ---
    df['Price Change %'] = (df['Binance_Close'] - df['Binance_Close'].shift(60)) / df['Binance_Close'].shift(60) * 100
    reference_price = df['Binance_Close'].shift(60).iloc[-1]
    
    df['Signal'] = df['Price Change %'].apply(generate_signal)
    df['Price Change %'] = df['Price Change %'].round(2).astype(str) + '%'
    # df['Binance_Close'] = 1 min resolution
    # df['Binance_Close'].shift(60) - This shifts the close price 60 rows back, which is 60 minutes ago, because your data is 1-minute candles
    # df['Binance_Close'] - df['Binance_Close'].shift(60) - This computes the price difference between now and 60 minutes ago

    if 'header_printed' not in globals():
        #print(f"{'Time':<25} {'Binance_Close':<12} {'Price Change %':<15} {'Signal'}")
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

    # --- Plotting ---
    plt.close('all')
    plt.clf()
    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df['Binance_Close'], label='Binance BTC-USDT', color='orange')

    # Plot BUY/SELL markers
    plt.scatter(df[df['Signal'] == 'BUY'].index, df[df['Signal'] == 'BUY']['Binance_Close'],
                label='BUY', color='green', marker='^')
    plt.scatter(df[df['Signal'] == 'SELL'].index, df[df['Signal'] == 'SELL']['Binance_Close'],
                label='SELL', color='red', marker='v')

    plt.title("Binance BTC Price with Buy/Sell Signals (Last 2 Hours)")
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.pause(300)
