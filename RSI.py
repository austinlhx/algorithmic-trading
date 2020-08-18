# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 22:52:09 2020

@author: Austin
"""


import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt

# Download historical data for required stocks
ticker = "AAPL"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())


#RSI is a momentum oscillator typically 14 days
#Oscillates between 0 and 100, if over 70, it is overbought
#price goes down, if under 30,shares goes up
def RSI(DF,n):
    "function to calculate RSI"
    df = DF.copy()
    df['delta']=df['Adj Close'] - df['Adj Close'].shift(1)
    #finding day over day change
    df['gain']=np.where(df['delta']>=0,df['delta'],0)
    #np where is if(condition) this, otherwise this
    df['loss']=np.where(df['delta']<0,abs(df['delta']),0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    #taking column from df, simply convert to list
    loss = df['loss'].tolist()
    for i in range(len(df)):
        if i < n:
            #if i is less than the period simply append NaN
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            #i == n, first value, only for that val we get the SMA
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            #When i is greater than period, we use formula 
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain']=np.array(avg_gain) #then append into a df
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    #calculate relative strength
    df['RSI'] = 100 - (100/(1+df['RS']))
    #calculate rsi
    return df['RSI']#return rsi column

# Calculating RSI without using loop
def rsi(df, n):
    "function to calculate RSI"
    delta = df["Adj Close"].diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[n-1]] = np.mean( u[:n]) # first value is average of gains
    u = u.drop(u.index[:(n-1)])
    d[d.index[n-1]] = np.mean( d[:n]) # first value is average of losses
    d = d.drop(d.index[:(n-1)])
    rs = u.ewm(com=n,min_periods=n).mean()/d.ewm(com=n,min_periods=n).mean()
    return 100 - 100 / (1+rs)

RSI(ohlcv, 14).iloc[-20:].plot()
#n is periods of where we want to calculate rsi