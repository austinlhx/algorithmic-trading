# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 15:11:40 2020

@author: Austin
"""


#Maximum Drawdown & Calmar Ratio

#Max Drawdown
#Looks at the largest percentage drop in asset price over a 
#specified time period
#Peak vs Trouph

#Calmar Ratio
#Ratio of CAGR and Max drawdown, measure of risk adj. return
#CAGR annual cumulative growth return


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
#CAGR aka average returns of a portfolio

def volatility(DF):
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)
    #252 for daily volatility (252 trading days per year)
    #52 for weekly volatility (52 trading weeks in a year)
    #12 for monthly volatility (12 trading months per year)
    return vol
#volatility is essentially the standard dev

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

def max_dd(DF):
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["cum_return"].iloc[-100:].plot()
    #iloc[-100] show only last 100 rows
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd

def calmar(DF):
    df = DF.copy()
    clmr = CAGR(df)/max_dd(df)
    return clmr


    