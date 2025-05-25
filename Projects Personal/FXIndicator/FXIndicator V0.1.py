# Author: Adrian Orastean
# Date: 25 Mai 2025
# Description: Python script to create a simple indicator for financial data that fetches data from Yahoo Finance and plots it.
# offer you signal to buy or sell based on the custom strategy.
# Version: 0.1 - initial version using yahoo finance data
# pip install yfinance pandas matplotlib
#----------------------------------------------------------------------------------------------------------------------------------------------

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#  Load BTC 1-minute candles for past 1 day
btc = yf.download(tickers="BTC-USD", period="1d", interval="1m")

# Keep only last 120 minutes
btc = btc.last('120min')

# Calculate % price change over the past 60 minutes
btc['Price Change %'] = (btc['Close'] - btc['Close'].shift(60)) / btc['Close'].shift(60) * 100

# Generate trading signals
def generate_signal(change):
    if pd.isna(change):
        return None
    if change <= -3:
        return 'SELL'
    elif change >= 4:
        return 'BUY'
    else:
        return 'HOLD'

btc['Signal'] = btc['Price Change %'].apply(generate_signal)


# Print most recent values
print(btc[['Close', 'Price Change %', 'Signal']].tail(10))

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(btc.index, btc['Close'], label='BTC-USD Price')
plt.scatter(btc[btc['Signal'] == 'BUY'].index, btc[btc['Signal'] == 'BUY']['Close'], label='BUY', color='green', marker='^')
plt.scatter(btc[btc['Signal'] == 'SELL'].index, btc[btc['Signal'] == 'SELL']['Close'], label='SELL', color='red', marker='v')
plt.title("BTC Price with Buy/Sell Signals (Last 2 Hours)")
plt.xlabel("Time")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
