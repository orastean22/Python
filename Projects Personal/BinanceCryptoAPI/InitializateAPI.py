# app.py

from binance.client import Client

def main():
    # Replace these with your actual API keys
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    
    client = Client(api_key, api_secret)
    
    # Fetch the latest price for Bitcoin (BTC) in USDT
    btc_ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    print("BTC/USDT Price:", btc_ticker['price'])

if __name__ == "__main__":
    main()
