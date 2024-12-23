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
        "comment": "Trend Following Buy",
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
        "comment": "Trend Following Sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(order_request)
    print("Sell Order" + (" successful" if result.retcode == mt5.TRADE_RETCODE_DONE else f" failed. Error: {result.retcode}"))

# Fetch data and calculate indicators of trend
def fetch_data(ticker):
    print("Fetching historical data...")
    data = yf.download(ticker, period="1mo", interval="1h")
    data = data[['Adj Close']].rename(columns={'Adj Close': 'Price'})
    data['ShortSMA'] = data['Price'].rolling(window=10).mean()
    data['LongSMA'] = data['Price'].rolling(window=30).mean()
    return data

# Check conditions and place orders
def check_conditions(data):
    short_sma = data['ShortSMA'].iloc[-1]
    long_sma = data['LongSMA'].iloc[-1]
    live_price = data['Price'].iloc[-1]
    if short_sma > long_sma and live_price > short_sma:
        print(f"Buy signal: Short SMA ({short_sma}) > Long SMA ({long_sma}) and Live Price ({live_price}) > Short SMA")
        place_buy_order()
    elif short_sma < long_sma and live_price < short_sma:
        print(f"Sell signal: Short SMA ({short_sma}) < Long SMA ({long_sma}) and Live Price ({live_price}) < Short SMA")
        place_sell_order()

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
