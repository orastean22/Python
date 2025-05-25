# Author: Adrian Orastean
# Date: 25 Mai 2025
# Description: Python script to create a simple indicator for financial data that fetches data from Yahoo Finance and plots it.
# offer you signal to buy or sell based on the custom strategy.
# Version: 0.2 - added Binance data comparison
# pip install yfinance pandas matplotlib
# pip install python-binance
#----------------------------------------------------------------------------------------------------------------------------------------------

import yfinance as yf
from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz

# --- Binance Setup (no API key needed for public data) ---
client = Client()

# Get recent 1-minute klines for BTC/USDT from Binance (last 120 minutes)
klines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=120)
binance_df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
])


# Process Binance Data
binance_df['time'] = pd.to_datetime(binance_df['timestamp'], unit='ms')
binance_df['time'] = binance_df['time'].dt.tz_localize('UTC') 
binance_df.set_index('time', inplace=True)
binance_df['Binance_Close'] = binance_df['close'].astype(float)
binance_df = binance_df[['Binance_Close']]


# --- Yahoo Finance BTC-USD ---
btc_yahoo = yf.download("BTC-USD", period="1d", interval="1m")
# Flatten MultiIndex columns if needed
if isinstance(btc_yahoo.columns, pd.MultiIndex):
    btc_yahoo.columns = [col[0] if isinstance(col, tuple) else col for col in btc_yahoo.columns]

# Make index timezone-aware (UTC) to match Binance timestamps
if btc_yahoo.index.tz is None:
    btc_yahoo.index = btc_yahoo.index.tz_localize('UTC')
else:
    btc_yahoo.index = btc_yahoo.index.tz_convert('UTC')

now_utc = pd.Timestamp.now(tz='UTC') # Define a timezone-aware current time
btc_yahoo = btc_yahoo.loc[btc_yahoo.index >= now_utc - pd.Timedelta('120min')] # Filter to keep only the last 120 minutes
btc_yahoo = btc_yahoo[['Close']].rename(columns={'Close': 'Yahoo_Close'}) # Rename Close column


# --- Merge Both DataFrames ---
combined = pd.merge(btc_yahoo, binance_df, left_index=True, right_index=True, how='inner')


# --- Plot Both ---
plt.figure(figsize=(14, 6))
plt.plot(combined.index, combined['Yahoo_Close'], label="Yahoo Finance BTC-USD", color='blue')
plt.plot(combined.index, combined['Binance_Close'], label="Binance BTC-USDT", color='orange', linestyle='--')
plt.title("BTC 1-Minute Price: Yahoo Finance vs Binance")
plt.xlabel("Time")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()