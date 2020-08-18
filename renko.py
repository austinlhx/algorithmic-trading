# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 16:05:36 2020

@author: Austin
"""


import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt
from stocktrends import Renko



# Download historical data for required stocks
ticker = "AAPL"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())
df = ohlcv.copy()
#Average True Range implementation
def ATR(DF, n):
    df = DF.copy()
    df["H-L"] = abs(df['High'] - df['Low'])
    #high - low
    df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
    #high vs previous close
    df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
    #low vs previous close
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    #True range, calculate max of three range
    df['ATR'] = df['TR'].rolling(n).mean()
    #n is period of rolling mean, 20 is an option
    #df['ATR'] = df['TR].ewm(span=n, adjust=false, min_periods =n).mean()
    #above is to use exponential moving avg, but not used alot, SMA is better
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    #df2.dropna(inplace= True)
    return df2
#ATR is used as the brick size for the data
def renko_dataframe(DF):
    df = DF.copy()
    
    df.reset_index(inplace = True)
    #make index as a seperate column, convert index to column
    #adding this allows the date to be its own column
    
    #For renko, all we need to look at is a couple rows
    df = df.iloc[:,[0,1,2,3,5,6]]
    #only include columns 0,1,2,3,5,6
    
    df.columns = ["date", "open","high","low","close","volume"]
    #simply rename the columns, respectively
    
    renko_df = Renko(df)
    renko_df.brick_size = round(ATR(df,120)["ATR"][-1]) #use atr to assign bricksize
    #-1 takes the latest point/last point
    df2 = renko_df.get_ohlc_data()
    #shows the uptrend based on the bricksize
    
    #follow two bricks, if 2 false, going down, if 2 true going up