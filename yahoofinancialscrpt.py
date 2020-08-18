# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 15:48:08 2020

@author: Austin
"""

import pandas as pd
from yahoofinancials import YahooFinancials
import datetime as dt

all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "INTC"]

close_prices = pd.DataFrame()
end_date = (dt.date.today()).strftime('%Y-%m-%d')
beg_date = (dt.date.today()-dt.timedelta(1825)).strftime('%Y-%m-%d')
for ticker in all_tickers:
    yahoo_financials= YahooFinancials(ticker)
    json_obj = yahoo_financials.get_historical_price_data(beg_date, end_date, "daily")
    ohlv = json_obj[ticker]['prices']
    temp = pd.DataFrame(ohlv)[["formatted_date", "adjclose"]]#store ohlv into dataframe and take only the fornatted date and adjclose price
    temp.set_index("formatted_date", inplace=True) #make date as index instead of 0 1 2 3...
    temp.dropna(inplace=True) #drop NaN values
    close_prices[ticker] = temp['adjclose']
