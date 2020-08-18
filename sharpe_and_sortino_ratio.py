# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 00:31:25 2020

@author: Austin
"""


#Sharpe ratio is average return earned 
#in excess of the risk free rate per unit of volatility
#sharpe ratio better than 1 is good, 2 is great, 3 excellent
#Sortino ratio is variation of sharpe ratio takes into account
#sd of only negative returns

#sharpe ratio fails to distinguish up and down fluctuation, 
#sortino makes than distinction and only considers harmful volatility

# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:53:18 2020

@author: Austin
"""


import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

ticker = "^GSPC"
SnP = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())

DF = SnP.copy()
def CAGR(DF):
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()
    #cumprod is cumulative product
    #shows you the pct change of your initial investment
    
    #n is the power that we will raise the ratio to
    n = len(df)/252 #252 is the number of trading days in a year
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    #[-1] latest value
    return CAGR

def volatility(DF):
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)
    #252 for daily volatility (252 trading days per year)
    #52 for weekly volatility (52 trading weeks in a year)
    #12 for monthly volatility (12 trading months per year)
    return vol

def sharpe(Df, rf): #rf is risk free 
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr

def sortino(Df, rf):
    df = Df.copy()
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    neg_vol = df[df["daily_ret"]<0]["daily_ret"].std() * np.sqrt(252)
    #this selects all the numbers which match our condition, so less than 0
    sr = (CAGR(df) - rf)/neg_vol 
    #neg_vol is negative volitility
    return sr

sortino(SnP, 0.055)
#0.055 was the current risk-free rate