# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 12:26:42 2020

@author: Austin
"""

import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt

# Download historical data for required stocks
ticker = "AAPL"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())

#ADX meassures strength of trends
#0-100 bonds, 0-25 weak, 25-50 strong, 50-75 very string, 75 extremely string
#Does not discuss direction


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

#Average Directional Index


def ADX(DF,n):
    "function to calculate ADX"
    df2 = DF.copy()
    df2['TR'] = ATR(df2,n)['TR'] #the period parameter of ATR function does not matter because period does not influence TR calculation
    df2['DMplus']=np.where((df2['High']-df2['High'].shift(1))>(df2['Low'].shift(1)-df2['Low']),df2['High']-df2['High'].shift(1),0)
    #above where is an if statement, simply if high - prev high > low - prev low, return high- prev high, else 0
    df2['DMplus']=np.where(df2['DMplus']<0,0,df2['DMplus'])
    df2['DMminus']=np.where((df2['Low'].shift(1)-df2['Low'])>(df2['High']-df2['High'].shift(1)),df2['Low'].shift(1)-df2['Low'],0)
    #same idea as DM plus
    df2['DMminus']=np.where(df2['DMminus']<0,0,df2['DMminus'])
    TRn = []#empty list due to inconsistency after first value
    DMplusN = []
    DMminusN = []
    TR = df2['TR'].tolist()#convert each to a list
    DMplus = df2['DMplus'].tolist()
    DMminus = df2['DMminus'].tolist()
    for i in range(len(df2)):
        if i < n:#if the day is less than the periods, it is nan, thus append nan
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == n:#simple rolling sum for the first period
            TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
            DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
            DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
        elif i > n:#smoothing sum function after the first period
            TRn.append(TRn[i-1] - (TRn[i-1]/n) + TR[i])
            DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/n) + DMplus[i])
            DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/n) + DMminus[i])
    df2['TRn'] = np.array(TRn)#populate the lists
    df2['DMplusN'] = np.array(DMplusN)
    df2['DMminusN'] = np.array(DMminusN)
    df2['DIplusN']=100*(df2['DMplusN']/df2['TRn'])
    #found these columns simply using the formula
    df2['DIminusN']=100*(df2['DMminusN']/df2['TRn'])
    df2['DIdiff']=abs(df2['DIplusN']-df2['DIminusN'])
    df2['DIsum']=df2['DIplusN']+df2['DIminusN']
    df2['DX']=100*(df2['DIdiff']/df2['DIsum'])
    #simple take division of two formula
    ADX = [] #ADX has inconsistent formula so we gotta convert
    DX = df2['DX'].tolist()
    for j in range(len(df2)):
        if j < 2*n-1:
            #value of n is not 14, we need to have a valid 14 values
            #so for a 14 day period it is 27, or 14 + 13
            ADX.append(np.NaN)
        elif j == 2*n-1:
            ADX.append(df2['DX'][j-n+1:j+1].mean())
            #mean of the last 27-14+1, or last 14 days : 28, the past 14 numbers
        elif j > 2*n-1:
            ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
    df2['ADX']=np.array(ADX)
    return df2['ADX']

ADX(ohlcv, 14).iloc[:-100].plot()