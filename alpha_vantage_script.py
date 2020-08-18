# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 18:16:09 2020

@author: Austin
"""


from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time

keyP = "JCGJXX4Q2LDHX5ZV"
ts = TimeSeries(key=keyP, output_format='pandas')
data = ts.get_daily(symbol='EURUSD', outputsize='full')[0] 
#data is a dataframe
data.columns = ['open', 'high', 'low', 'close', 'volume']
data = data.iloc[::-1] #reverses dataframe

all_tickers = ['AAPL', 'MSFT', 'CSCO', 'AMZN', 'GOOG', 'FB']
close_prices = pd.DataFrame()
api_call_count = 0
for ticker in all_tickers:
    start_time = time.time()
    ts = TimeSeries(key=keyP, output_format='pandas')
    data = ts.get_daily(symbol=ticker, outputsize='compact')[0]
    api_call_count+=1
    data.columns = ['open', 'high', 'low', 'close', 'volume']
    data = data.iloc[::-1]
    close_prices[ticker] = data["close"]
    if api_call_count == 5:
        api_call_count = 0
        time.sleep(60 - (time.time() - start_time))