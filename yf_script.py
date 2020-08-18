# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 16:24:26 2020

@author: Austin
"""

import datetime as dt
import yfinance as yf
import pandas as pd



stocks = ["AMZN", "MSFT", "INTC", "GOOG", "INFY.NS", "3988.HK"]
start = dt.datetime.today() - dt.timedelta(30) #today - 30 days
end = dt.datetime.today()
cl_price = pd.DataFrame() 
ohlcv_data = {}

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end)["Adj Close"]
#save only adj close

for ticker in stocks:
    ohlcv_data[ticker] = yf.download(ticker, start, end)
    
print(ohlcv_data["MSFT"]["Open"])
    
    