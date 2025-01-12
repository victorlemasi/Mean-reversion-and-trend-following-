# Mean-reversion-and-trend-following-
downloads historical data (30 days in this case), calculates the moving average and standard deviation, and determines if the current price is far enough from the mean to trigger a buy or sell signal.
A buy signal is triggered if the current price is more than 2 standard deviations below the mean, while a sell signal is triggered if the price is more than 2 standard deviations above the mean.
The script uses the .rolling(window=20) method to calculate a 20-day rolling window moving average and standard deviation. You can adjust the window size depending on your strategy's need
