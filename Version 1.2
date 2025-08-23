import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from datetime import datetime, timedelta

def mt5_login(login, password, server="MetaQuotes-Demo"):
    """
    Initializes and logs in to the MT5 terminal.
    
    Args:
        login (int): The MT5 account login ID.
        password (str): The MT5 account password.
        server (str): The MT5 server name.
        
    Returns:
        bool: True if login is successful, False otherwise.
    """
    if not mt5.initialize():
        print("MT5 initialization failed")
        return False
        
    # Login to MT5
    login_result = mt5.login(login=login, 
                           password=password,
                           server=server)
    
    if login_result:
        print("MT5 login successful")
        account_info = mt5.account_info()
        if account_info is not None:
            print(f"Account: {account_info.login}")
            print(f"Balance: {account_info.balance}")
            print(f"Equity: {account_info.equity}")
        return True
    else:
        print("MT5 login failed")
        mt5.shutdown()
        return False

def get_mt5_data(symbol, timeframe=mt5.TIMEFRAME_D1, number_of_bars=1000):
    """
    Gets historical data from MT5 and returns it as a pandas DataFrame.
    
    Args:
        symbol (str): The financial instrument symbol (e.g., "EURUSD").
        timeframe (int): The MT5 timeframe constant (e.g., mt5.TIMEFRAME_D1).
        number_of_bars (int): The number of historical bars to retrieve.
        
    Returns:
        pd.DataFrame: A DataFrame containing the historical data.
    """
    # Get the bars
    bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, number_of_bars)
    
    # Convert to DataFrame
    df = pd.DataFrame(bars)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Rename columns to match the strategy's requirements
    df = df.rename(columns={'time': 'date',
                          'open': 'open',
                          'high': 'high',
                          'low': 'low',
                          'close': 'close'})
    
    return df

def calculate_atr(high, low, close, period=42):
    """
    Calculates the Average True Range (ATR).
    
    Args:
        high (pd.Series): The series of high prices.
        low (pd.Series): The series of low prices.
        close (pd.Series): The series of close prices.
        period (int): The ATR calculation period.
        
    Returns:
        pd.Series: The calculated ATR values.
    """
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)
    
    # Calculate True Range
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr

def trend_following_strategy(df):
    """
    Implements a trend following strategy based on new all-time highs
    with an ATR-based profit target.
    
    Args:
        df (pd.DataFrame): The DataFrame with OHLCV data.
        
    Returns:
        pd.DataFrame: The DataFrame with added strategy signals and metrics.
    """
    # Create copy of dataframe
    signals = df.copy()
    
    # Calculate ATR
    signals['ATR'] = calculate_atr(signals['high'], 
                                 signals['low'], 
                                 signals['close'])
    
    # Calculate running maximum (all-time high)
    signals['running_max'] = signals['high'].expanding().max()
    
    # Generate entry signals (a new high is a potential entry)
    signals['new_high'] = signals['running_max'] != signals['running_max'].shift(1)
    signals['entry_signal'] = signals['new_high'].shift(1)
    
    # Calculate profit target (10 * ATR above entry price)
    signals['profit_target'] = np.nan
    
    # Initialize position tracking
    signals['position'] = 0
    signals['entry_price'] = np.nan
    
    # Track active trades
    current_position = 0
    current_target = np.nan
    current_entry = np.nan
    
    for i in range(1, len(signals)):
        if signals['entry_signal'].iloc[i] and current_position == 0:
            # Enter new position
            current_position = 1
            current_entry = signals['open'].iloc[i]
            # Set profit target
            current_target = current_entry + (10 * signals['ATR'].iloc[i])
            
        if current_position == 1:
            # Check if profit target is hit
            if signals['high'].iloc[i] >= current_target:
                # Profit target hit
                current_position = 0
                current_target = np.nan
                current_entry = np.nan
            
        signals['position'].iloc[i] = current_position
        signals['profit_target'].iloc[i] = current_target
        signals['entry_price'].iloc[i] = current_entry
    
    # Calculate returns
    signals['returns'] = np.where(signals['position'].shift(1) == 1,
                                signals['close'] / signals['close'].shift(1) - 1,
                                0)
    
    # Calculate cumulative returns
    signals['cumulative_returns'] = (1 + signals['returns']).cumprod()
    
    return signals

def place_mt5_order(symbol, order_type, volume, price=0.0, comment="Trend Following"):
    """
    Places a market order in MT5.
    
    Args:
        symbol (str): The symbol to trade.
        order_type (int): The MT5 order type (e.g., mt5.ORDER_TYPE_BUY).
        volume (float): The trade volume.
        price (float): The order price (used for limit/stop orders).
        comment (str): A comment for the trade.
        
    Returns:
        mt5.TradeResult: The result of the order operation.
    """
    point = mt5.symbol_info(symbol).point
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "deviation": 20,
        "magic": 234000,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    return result

def live_trading(symbol, timeframe=mt5.TIMEFRAME_D1, volume=0.1):
    """
    Runs the strategy live and places orders on MT5 based on signals.
    
    Args:
        symbol (str): The financial instrument symbol.
        timeframe (int): The MT5 timeframe constant.
        volume (float): The trade volume.
    """
    # Get latest data
    df = get_mt5_data(symbol, timeframe)
    
    # Run strategy
    signals = trend_following_strategy(df)
    
    # Get latest signal
    current_position = signals['position'].iloc[-1]
    previous_position = signals['position'].iloc[-2]
    
    # Check for trade signals
    if current_position == 1 and previous_position == 0:
        # Entry signal (open a new long position)
        result = place_mt5_order(symbol, 
                               mt5.ORDER_TYPE_BUY, 
                               volume, 
                               comment="Trend Following Entry")
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Buy order placed successfully at {result.price}")
            
    elif current_position == 0 and previous_position == 1:
        # Exit signal (close an open long position)
        result = place_mt5_order(symbol, 
                               mt5.ORDER_TYPE_SELL, 
                               volume, 
                               comment="Trend Following Exit")
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Sell order placed successfully at {result.price}")

def backtest_strategy(df):
    """
    Runs a backtest on the strategy and prints performance metrics.
    
    Args:
        df (pd.DataFrame): The DataFrame with OHLCV data.
        
    Returns:
        pd.DataFrame: The DataFrame with backtest results.
    """
    results = trend_following_strategy(df)
    
    # Calculate metrics
    total_returns = results['cumulative_returns'].iloc[-1] - 1
    annual_returns = (1 + total_returns) ** (252 / len(results)) - 1
    
    # Calculate maximum drawdown
    rolling_max = results['cumulative_returns'].expanding().max()
    drawdowns = results['cumulative_returns'] / rolling_max - 1
    max_drawdown = drawdowns.min()
    
    # Calculate win rate
    trades = results[results['position'] != results['position'].shift(1)]
    # A complete trade is an entry and an exit, so divide by 2
    total_trades = len(trades) / 2  
    wins = len(trades[trades['returns'] > 0])
    win_rate = wins / total_trades if total_trades > 0 else 0
    
    print(f"Total Return: {total_returns:.2%}")
    print(f"Annualized Return: {annual_returns:.2%}")
    print(f"Maximum Drawdown: {max_drawdown:.2%}")
    print(f"Win Rate: {win_rate:.2%}")
    print(f"Total Trades: {total_trades:.0f}")
    
    return results

# Main execution block
if __name__ == "__main__":
    # You MUST replace these with your actual MT5 account credentials
    login = 123456789
    password = "your_password"
    server = "MetaQuotes-Demo"
    
    # Login to MT5
    if mt5_login(login, password, server):
        # Define the trading symbol
        symbol = "EURUSD"
        
        # Get historical data for the backtest
        df = get_mt5_data(symbol)
        
        # Run the backtest and print the results
        print("\n--- Backtest Results ---")
        backtest_results = backtest_strategy(df)
        
        # Run the live trading logic (this would be in a loop for continuous trading)
        print("\n--- Live Trading Check ---")
        live_trading(symbol)
        
        # Shutdown the MT5 connection when done
        mt5.shutdown()
