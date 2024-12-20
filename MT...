# Copyright 2024, MetaQuotes Ltd.
# https://www.mql5.com

from datetime import datetime
import MetaTrader5 as mt5
import yfinance as yf
import pandas as pd
import time

# Define broker credentials
broker_login = 123456  # Replace with your broker's MetaTrader login ID
broker_password = "yourpassword"  # Replace with your broker's password
broker_server = "yourbroker-server"  # Replace with your broker's server name

# Initialize MetaTrader 5 and log in to your broker
def initialize_broker():
    if not mt5.initialize():
        print("MetaTrader 5 initialization failed")
        quit()
    else:
        print("MetaTrader 5 initialized")
    
    authorized = mt5.login(login=broker_login, password=broker_password, server=broker_server)
    if authorized:
        print("Logged in to the broker successfully")
    else:
        print(f"Failed to log in to the broker. Error code: {mt5.last_error()}")

# Function to fetch historical data from Yahoo Finance
def fetch_historical_data(ticker):
    print("\nFetching historical data from Yahoo Finance...")
    data = yf.download(ticker, start="2023-01-01", end="2023-12-01", interval="1d")
    data = data[['Adj Close']].rename(columns={'Adj Close': 'Price'})
    
    # Mean Reversion indicators
    window_size = 126  # Approx. 6 months of trading days
    data['SMA'] = data['Price'].rolling(window=window_size).mean()  # Simple Moving Average
    data['StdDev'] = data['Price'].rolling(window=window_size).std()  # Standard Deviation
    data['UpperBand'] = data['SMA'] + 2 * data['StdDev']  # Upper Band for Mean Reversion
    data['LowerBand'] = data['SMA'] - 2 * data['StdDev']  # Lower Band for Mean Reversion
    
    # Trend Following indicators
    short_window = 42  # Approx. 2 months of trading days
    long_window = 126  # Approx. 6 months of trading days
    data['ShortSMA'] = data['Price'].rolling(window=short_window).mean()  # Short-term SMA
    data['LongSMA'] = data['Price'].rolling(window=long_window).mean()  # Long-term SMA
    
    return data

# Function to fetch live data from Yahoo Finance
def fetch_live_data(ticker):
    print("\nFetching live data from Yahoo Finance...")
    live_data = yf.download(tickers=ticker, period="1d", interval="1m")
    live_data = live_data[['Adj Close']].rename(columns={'Adj Close': 'Price'})
    return live_data

# Compare historical data with live data
def compare_historical_with_live(historical, live):
    print("\n--- Comparing Historical and Live Data ---")
    
    # Get the last row from historical data
    last_historical = historical.iloc[-1]
    
    # Get the most recent live price
    live_price = live['Price'].iloc[-1]
    
    # Mean Reversion Strategy
    # Check if the live price is significantly above or below the mean (SMA) using the upper and lower bands
    if live_price < last_historical['LowerBand']:
        print(f"Buy signal: Live price {live_price} is below the lower band ({last_historical['LowerBand']}).")
    elif live_price > last_historical['UpperBand']:
        print(f"Sell signal: Live price {live_price} is above the upper band ({last_historical['UpperBand']}).")
    
    # Trend Following Strategy
    # Determine if the short-term SMA is above or below the long-term SMA to identify the trend
    short_sma = historical['ShortSMA'].iloc[-1]
    long_sma = historical['LongSMA'].iloc[-1]
    
    if short_sma > long_sma and live_price > short_sma:
        print(f"Trend UP signal: Live price {live_price} is above Short SMA ({short_sma}), and Short SMA is above Long SMA ({long_sma}).")
    elif short_sma < long_sma and live_price < short_sma:
        print(f"Trend DOWN signal: Live price {live_price} is below Short SMA ({short_sma}), and Short SMA is below Long SMA ({long_sma}).")
    else:
        print("No significant trading signal detected.")

# Main execution
def main():
    ticker = "AAPL"  # Stock symbol for Apple Inc.
    
    # Initialize broker
    initialize_broker()
    
    # Fetch historical data once
    historical_data = fetch_historical_data(ticker)
    
    # Continuous loop for live updates
    while True:
        try:
            # Fetch live data
            live_data = fetch_live_data(ticker)
            
            # Compare historical data with live data
            compare_historical_with_live(historical_data, live_data)
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Sleep for 5 minutes
        print("Waiting for 5 minutes before the next check...")
        time.sleep(300)

# Start the program
if __name__ == "__main__":
    main()
