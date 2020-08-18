# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 14:38:38 2020

@author: Austin
"""


import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt

# Download historical data for required stocks
ticker = "MSFT"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())
def MACD(Df, a, b, c):
    df = Df.copy()
    #ewm = exponential moving average
    df["MA_Fast"]=df["Adj Close"].ewm(span=a,min_periods=a).mean() #calculate fast moving average
    df["MA_Slow"]=df["Adj Close"].ewm(span=b,min_periods=b).mean() #calculate slow moving average
    df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
    df["Signal"] = df["MACD"].ewm(span=c, min_periods=c).mean()
    df.dropna(inplace=True)
    #Signal Line
    #typical time of MA_fast is 12, MA_Slow is 26, signal line is 9
    return (df["MACD"], df["Signal"])

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