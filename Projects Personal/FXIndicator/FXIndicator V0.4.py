# Author: Adrian Orastean
# Date: 25 Mai 2025
# Description: Python script to create a simple indicator for financial data that fetches data from Yahoo Finance and plots it.
# offer you signal to buy or sell based on the custom strategy.
# Version: 0.4  - added Binance data + plotting + strategy for buy/sell signals.
# pip install yfinance pandas matplotlib
# pip install python-binance

#----STRATEGY-----------------------------------------------------------------------------------------------------------------------------------
# BUY signal:  if BTC price rise > +3% in last 60 minutes
# SELL signal: if BTC price drop < -4% in last 60 minutes
#----------------------------------------------------------------------------------------------------------------------------------------------

from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

# --- Binance Setup (no API key needed) ---
client = Client()

# Get recent 1-minute candles for last 2 hours
klines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=120)

# Convert to DataFrame
df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
])

# Format time & price
df['time'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC')
df.set_index('time', inplace=True)
df['Binance_Close'] = df['close'].astype(float)
df = df[['Binance_Close']]

# --- Apply Strategy: % Change Over Past 60 Minutes ---
df['Price Change %'] = (df['Binance_Close'] - df['Binance_Close'].shift(60)) / df['Binance_Close'].shift(60) * 100

def generate_signal(change):
    if pd.isna(change):
        return None
    if change > 3:
        return 'BUY'
    elif change < -4:
        return 'SELL'
    else:
        return 'HOLD'

df['Signal'] = df['Price Change %'].apply(generate_signal)
df['Price Change %'] = df['Price Change %'].round(2).astype(str) + '%'


print(df[['Binance_Close', 'Price Change %', 'Signal']].tail(10))
# --- Plotting ---
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
plt.show()











































