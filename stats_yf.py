# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 17:48:55 2020

@author: Austin
"""


import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download historical data for required stocks
tickers = ["MSFT","AMZN","AAPL","CSCO","IBM","FB"]

start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
close_prices = pd.DataFrame() # empty dataframe which will be filled with closing prices of each stock

# looping over tickers and creating a dataframe with close prices
for ticker in tickers:
    close_prices[ticker] = yf.download(ticker,start,end)["Adj Close"]
    
# Mean, Median, Standard Deviation, daily return
close_prices.mean() # prints mean stock price for each stock
close_prices.median() # prints median stock price for each stock
close_prices.std() # prints standard deviation of stock price for each stock

daily_return = close_prices.pct_change() # Creates dataframe with daily return for each stock
#pct_change is close_prices/close_prices.shift(1)-1 shifts the entire data frame by 1, meaning the 26th price becomes 27th price...etc
daily_return.mean() # prints mean daily return for each stock
daily_return.std() # prints standard deviation of daily returns for each stock
daily_return.rolling(window=20, min_periods=1).mean()
daily_return.rolling(window=20, min_periods=1).std()
daily_return.ewm(span=20, min_periods=20).mean()
daily_return.ewm(span=20, min_periods=20).std()

close_prices.plot()
cp_standardized = (close_prices - close_prices.mean())/close_prices.std()
cp_standardized.plot()

close_prices.plot(subplots=True, layout = (3,2), title = "Tech Stock Price Evolution", grid = True)

#fig number of charts trying to create, ax axis
fig, ax = plt.subplots()
plt.style.available
plt.style.use('ggplot')
ax.set(title="Daily return on tech stocks", xlabel="Tech Stocks", ylabel="Daily Returns")
plt.bar(daily_return.columns, daily_return.mean())
#.mean default cals col mean