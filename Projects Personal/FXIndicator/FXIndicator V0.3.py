# Author: Adrian Orastean
# Date: 25 Mai 2025
# Description: Python script to create a simple indicator for financial data that fetches data from Yahoo Finance and plots it.
# offer you signal to buy or sell based on the custom strategy.
# Version: 0.3 - added Binance data comparison and simulated Google Finance data
# pip install yfinance pandas matplotlib
# pip install python-binance
#----------------------------------------------------------------------------------------------------------------------------------------------

import yfinance as yf
from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

# --- Binance Data (UTC) ---
client = Client()
klines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=120)
binance_df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
])
binance_df['time'] = pd.to_datetime(binance_df['timestamp'], unit='ms').dt.tz_localize('UTC')
binance_df.set_index('time', inplace=True)
binance_df['Binance_Close'] = binance_df['close'].astype(float)
binance_df = binance_df[['Binance_Close']]

# --- Yahoo Finance BTC-USD (UTC) ---
btc_yahoo = yf.download("BTC-USD", period="1d", interval="1m")
if isinstance(btc_yahoo.columns, pd.MultiIndex):
    btc_yahoo.columns = [col[0] for col in btc_yahoo.columns]
btc_yahoo.index = btc_yahoo.index.tz_convert('UTC') if btc_yahoo.index.tz else btc_yahoo.index.tz_localize('UTC')
now_utc = pd.Timestamp.now(tz='UTC')
btc_yahoo = btc_yahoo.loc[btc_yahoo.index >= now_utc - pd.Timedelta('120min')]
btc_yahoo = btc_yahoo[['Close']].rename(columns={'Close': 'Yahoo_Close'})

# --- Simulate Google Finance using BTC-EUR (converted to USD) ---
btc_google = yf.download("BTC-EUR", period="1d", interval="1m")
if isinstance(btc_google.columns, pd.MultiIndex):
    btc_google.columns = [col[0] for col in btc_google.columns]
btc_google.index = btc_google.index.tz_convert('UTC') if btc_google.index.tz else btc_google.index.tz_localize('UTC')
btc_google = btc_google.loc[btc_google.index >= now_utc - pd.Timedelta('120min')]
btc_google = btc_google[['Close']].rename(columns={'Close': 'Google_Close'})
btc_google['Google_Close'] *= 1.085  # Rough EUR to USD conversion

# --- Merge All Data Sources ---
combined = btc_yahoo.join([binance_df, btc_google], how='inner')

# --- Plot ---
plt.figure(figsize=(14, 6))
plt.plot(combined.index, combined['Yahoo_Close'], label="Yahoo Finance BTC-USD", color='blue')
plt.plot(combined.index, combined['Binance_Close'], label="Binance BTC-USDT", color='orange', linestyle='--')
plt.plot(combined.index, combined['Google_Close'], label="Google Finance BTC (Simulated)", color='green', linestyle=':')
plt.title("BTC 1-Minute Price: Yahoo vs Binance vs Google (Simulated via BTC-EUR)")
plt.xlabel("Time")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()