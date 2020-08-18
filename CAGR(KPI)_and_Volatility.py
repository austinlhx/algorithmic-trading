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
#CAGR is annual cumulative growth return
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
    