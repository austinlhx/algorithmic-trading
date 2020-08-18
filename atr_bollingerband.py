# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 15:35:01 2020

@author: Austin
"""


import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt

# Download historical data for required stocks
ticker = "ROKU"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())

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


def BollBnd(DF, n):
    df = DF.copy()
    #Moving Average
    df["MA"] = df['Adj Close'].rolling(n).mean()
    #bollinger band the up line
    #2 times the std
    df["BB_up"] = df["MA"] + 2*df['MA'].rolling(n).std()
    df["BB_dn"] = df["MA"] - 2*df['MA'].rolling(n).std()
    df["BB_width"] = df['BB_up'] - df['BB_dn']
    df.dropna(inplace = True)
    return df

BollBnd(ohlcv, 20).iloc[-100:, [-4,-3,-2]].plot()
#iloc only gets the relevant columns with 
#-100 is last 100 points