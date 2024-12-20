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

# Define trade parameters
symbol = "AAPL"  # Trading symbol
lot_size = 0.1  # Lot size for each trade
slippage = 5  # Maximum slippage allowed (points)

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
        quit()

# Function to place a buy order
def place_buy_order():
    print("Placing Buy Order...")
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"Failed to get tick data for {symbol}")
        return

    order_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": tick.ask,
        "slippage": slippage,
        "magic": 123456,
        "comment": "Mean Reversion/Trend Following Buy Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(order_request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print("Buy Order placed successfully")
    else:
        print(f"Buy Order failed. Error code: {result.retcode}")

# Function to place a sell order
def place_sell_order():
    print("Placing Sell Order...")
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"Failed to get tick data for {symbol}")
        return

    order_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_SELL,
        "price": tick.bid,
        "slippage": slippage,
        "magic": 123456,
        "comment": "Mean Reversion/Trend Following Sell Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(order_request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print("Sell Order placed successfully")
    else:
        print(f"Sell Order failed. Error code: {result.retcode}")

# Function to fetch historical data using Yahoo Finance API
def fetch_historical_data(ticker):
    print("\nFetching historical data from Yahoo Finance...")
    data = yf.download(ticker, start="2023-01-01", end="2023-12-01", interval="1d")
    data = data[['Adj Close']].rename(columns={'Adj Close': 'Price'})
    
    # Mean Reversion indicators
    window_size = 126  # Approx. 6 months of trading days
    data['SMA'] = data['Price'].rolling(window=window_size).mean()  # Simple Moving Average
    data['StdDev'] = data['Price'].rolling(window=window_size).std()  # Standard Deviation
    data['UpperBand'] = data['SMA'] + 2 * data['StdDev']  # Upper Band
    data['LowerBand'] = data['SMA'] - 2 * data['StdDev']  # Lower Band
    
    # Trend Following indicators
    short_window = 42  # Approx. 2 months
    long_window = 126  # Approx. 6 months
    data['ShortSMA'] = data['Price'].rolling(window=short_window).mean()
    data['LongSMA'] = data['Price'].rolling(window=long_window).mean()
    
    return data

# Function to fetch live data using Yahoo Finance API
def fetch_live_data(ticker):
    print("\nFetching live data from Yahoo Finance...")
    live_data = yf.download(tickers=ticker, period="1d", interval="1m")
    live_data = live_data[['Adj Close']].rename(columns={'Adj Close': 'Price'})
    return live_data

# Compare historical data with live data and place orders
def compare_historical_with_live(historical, live):
    print("\n--- Comparing Historical and Live Data ---")
    
    # Get the last row from historical data
    last_historical = historical.iloc[-1]
    
    # Get the most recent live price
    live_price = live['Price'].iloc[-1]
    
    # Mean Reversion Strategy
    if live_price < last_historical['LowerBand']:
        print(f"Buy signal: Live price {live_price} below lower band ({last_historical['LowerBand']}).")
        place_buy_order()
    elif live_price > last_historical['UpperBand']:
        print(f"Sell signal: Live price {live_price} above upper band ({last_historical['UpperBand']}).")
        place_sell_order()
    
    # Trend Following Strategy
    short_sma = historical['ShortSMA'].iloc[-1]
    long_sma = historical['LongSMA'].iloc[-1]
    
    if short_sma > long_sma and live_price > short_sma:
        print(f"Trend UP signal: Live price {live_price} above Short SMA ({short_sma}) and Short SMA above Long SMA ({long_sma}).")
        place_buy_order()
    elif short_sma < long_sma and live_price < short_sma:
        print(f"Trend DOWN signal: Live price {live_price} below Short SMA ({short_sma}) and Short SMA below Long SMA ({long_sma}).")
        place_sell_order()

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
            
            # Compare historical data with live data and place orders
            compare_historical_with_live(historical_data, live_data)
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Sleep for 5 minutes
        print("Waiting for 5 minutes before the next check...")
        time.sleep(300)

# Start the program
if __name__ == "__main__":
    main()
