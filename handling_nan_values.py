# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:28:51 2020

@author: Austin
"""


import datetime as dt
import yfinance as yf
import pandas as pd

stocks = ["AMZN", "MSFT", "FB", "GOOG"]
start = dt.datetime.today() - dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame()
ohlcv_data = {}

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start,end)["Adj Close"]

#cl_price.fillna({"FB": 0, "GOOG": 1}) #fill nan values with something
cl_price.fillna(method='bfill', axis = 0, inplace=True) 
#inplace works as like a cl_price = cl_price...
#fill the nan values based on axis, 1 copies rows, 0 copies column, 0 default
cl_price.dropna(method='bfill', axis = 0, inplace=True) 
#dropna removes values, removes columns? or rows? based on axis
#cl_price.dropna(axis = 1, how= 'all')
#drop na only if each row is empty
