# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 17:21:44 2020

@author: Austin
"""


#Rising OBV leads to higher prices
#Dropping OBV leads to lower prices
#OBV is a leading market indicator, for predictions
#BUT LOTS OF FALSE SIGNALS
#OBV generally used with MACD

#OBV uses volume information and Direction(If (todays price > yesterdays price) 1, -1)
#Direction is either -1, or 1
#Then calculate Vol * direction
#OBV is then the cumulative sum 

import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt

# Download historical data for required stocks
ticker = "AAPL"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())

def OBV(DF):
    df = DF.copy()
    #calculate daily return
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['direction'] = np.where(df['daily_ret']>=0, 1, -1)
    #first direction is just 0
    df['direction'][0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['obv'] = df['vol_adj'].cumsum()#cumulative sum
    return df['obv']
    
OBV(ohlcv).iloc[-100:].plot()
    