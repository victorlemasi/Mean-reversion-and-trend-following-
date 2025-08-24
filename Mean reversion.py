from datetime import datetime
import MetaTrader5 as mt5
import yfinance as yf
import pandas as pd
import time

# Broker credentials
broker_login = 123456
broker_password = "yourpassword"
broker_server = "yourbroker-server"

# Trade parameters
symbol = "AAPL"
lot_size = 0.1
slippage = 5

# Initialize MetaTrader 5
def initialize_broker():
    if not mt5.initialize():
        print("MetaTrader 5 initialization failed")
        quit()
    authorized = mt5.login(login=broker_login, password=broker_password, server=broker_server)
    if authorized:
        print("Broker login successful")
    else:
        print(f"Broker login failed. Error: {mt5.last_error()}")
        quit()

# Place buy order
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
        "comment": "Mean Reversion Buy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(order_request)
    print("Buy Order" + (" successful" if result.retcode == mt5.TRADE_RETCODE_DONE else f" failed. Error: {result.retcode}"))

# Place sell order
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
        "comment": "Mean Reversion Sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(order_request)
    print("Sell Order" + (" successful" if result.retcode == mt5.TRADE_RETCODE_DONE else f" failed. Error: {result.retcode}"))

# Fetch data and calculate indicators for mean reversion 
def fetch_data(ticker):
    print("Fetching historical data...")
    data = yf.download(ticker, period="1mo", interval="1h")
    data = data[['Adj Close']].rename(columns={'Adj Close': 'Price'})
    data['SMA'] = data['Price'].rolling(window=20).mean()
    data['StdDev'] = data['Price'].rolling(window=20).std()
    data['UpperBand'] = data['SMA'] + 2 * data['StdDev']
    data['LowerBand'] = data['SMA'] - 2 * data['StdDev']
    return data

# Check conditions and place orders
def check_conditions(data):
    live_price = data['Price'].iloc[-1]
    upper_band = data['UpperBand'].iloc[-1]
    lower_band = data['LowerBand'].iloc[-1]
    if live_price > upper_band:
        print(f"Sell signal: {live_price} > Upper Band ({upper_band})")
        place_sell_order()
    elif live_price < lower_band:
        print(f"Buy signal: {live_price} < Lower Band ({lower_band})")
        place_buy_order()

# Main loop
def main():
    initialize_broker()
    while True:
        try:
            data = fetch_data(symbol)
            check_conditions(data)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(300)

if __name__ == "__main__":
    main()
