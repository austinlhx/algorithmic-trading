# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 18:15:05 2020

@author: Austin
"""
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt

def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    n = len(df)/12
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["mon_ret"].std() * np.sqrt(12)
    return vol

def sharpe(DF,rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr
    

def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd

tickers = ["MMM","AXP","T","BA","CAT","CVX","CSCO","KO", "XOM","GE","GS","HD",
           "IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV",
           "UTX","UNH","VZ","V","WMT","DIS"]



start = dt.datetime.today() - dt.timedelta(3650) #today - 30 days
end = dt.datetime.today()
cl_price = pd.DataFrame() 
ohlcv_data = {}

for ticker in tickers:
    ohlcv_data[ticker] = yf.download(ticker, start, end,interval="1mo")
    ohlcv_data[ticker].dropna(inplace = True)
    
tickers = ohlcv_data.keys() #have only the keys of our valid stocks


####################### Back Testing #######################

ohlc_dict = copy.deepcopy(ohlcv_data)
#deep copy avoids the original data to be tampered with

return_df = pd.DataFrame()
#This data frame will have columns of the stocks and returns

for ticker in tickers:
    print("calculating monthly return for ",ticker)
    ohlc_dict[ticker]["mon_ret"] = ohlc_dict[ticker]["Adj Close"].pct_change()
    return_df[ticker] = ohlc_dict[ticker]["mon_ret"]
#creating data frame with col being stocks and rows being monthly return

DF = return_df
m = 6
x = 3
i = 10
portfolio = ["MMM","AXP","T","BA","CAT","CVX"]


# function to calculate portfolio return iteratively
def pflio(DF,m,x):
    """Returns cumulative portfolio return
    DF = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""
    df = DF.copy()
    portfolio = [] #portfolio will be populated 
    monthly_ret = [0] #initialize with 0, since first value in pct is 0
    for i in range(1,len(df)):#traverse every row of dataframe
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i,:].mean())
            #df[portfolio] is just our info, the data frame
            #.iloc[i,:] will give the ith row of all our returns
            #then take the avg of each row to get our average return
            bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            #identify bad_stocks, sort the values by ascending, :x takes the first x amount
            #of stocks we want to remove
            portfolio = [t for t in portfolio if t not in bad_stocks]
            #this removes one list from another list, simply removing our bad_stocks from the 
            #normal list
        fill = m - len(portfolio)
        new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        #new_picks takes the entire list of stocks and then picks the top (fill) performing stocks
    
        portfolio = portfolio + new_picks
        print(portfolio)
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret),columns=["mon_ret"])
    #create a monthly return dataframe with a column of all dataframes
    return monthly_ret_df


#calculating overall strategy's KPIs
CAGR(pflio(return_df,6,3))
#Overall increase in price over a certain period of time

sharpe(pflio(return_df,6,3),0.025)
max_dd(pflio(return_df,6,3)) 

#calculating KPIs for Index buy and hold strategy over the same period
DJI = yf.download("^DJI",dt.date.today()-dt.timedelta(1900),dt.date.today(),interval='1mo')
DJI["mon_ret"] = DJI["Adj Close"].pct_change()
CAGR(DJI)
sharpe(DJI,0.025)
max_dd(DJI)

#visualization
fig, ax = plt.subplots()
plt.plot((1+pflio(return_df,6,3)).cumprod())
plt.plot((1+DJI["mon_ret"][2:].reset_index(drop=True)).cumprod())
plt.title("Index Return vs Strategy Return")
plt.ylabel("cumulative return")
plt.xlabel("months")
ax.legend(["Strategy Return","Index Return"])





























