# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 20:41:25 2020

@author: Austin
"""

import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt
import statsmodels.api as sm

#Calculate slope OLS(ordinary least squares) and linear regression


# Download historical data for required stocks
ticker = "AAPL"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())

#ser is a series

ser = ohlcv['Adj Close']
#n = 5 #how many consecutive points you want to find it for
# we want a column that calculates slope for every 5 points
def slope(ser, n):
    #initialize  empty list
    #for first 4 points we wont have any slope
    # first n-1 is 0 so the bottom here initialize three 0s for first three
    slopes = [i*0 for i in range(n-1)]
    for i in range(n, len(ser)+1):#range from n to length of series + 1
        y = ser[i-n:i]
        #5 - 5: 5, gives first 5 values of the series
        #i = n for first pass through, 
        x = np.array(range(n))
        y_scaled = (y - y.min())/(y.max() - y.min())
        #scaling is similar to standardization
        x_scaled = (x - x.min())/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)
        #add constant for y = mx + b, the b
        #add constant to x-axis, if not, it will use the origin, y = mx, rather than y = mx + b
        model = sm.OLS(y_scaled, x_scaled)
        #model is stats model , linear regression model
        results = model.fit()
        #results is a linear regression
        #results.summary()
        #shows the regression results, r squared, ols regression results
        slopes.append(results.params[-1]) #params to only append slope
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    #simply convert the radians to degrees by taking the tans of slopes -> get radians then radians to degrees
    return np.array(slope_angle)
    
def Slope(ser, n):
    ser = DF.copy()
    slopes = [i*0 for i in range(n-1)]

df = ohlcv.copy()
df["slope"] = slope(ohlcv["Adj Close"], 5)
df.iloc[-50:,[4,6]].plot(subplots=True, layout = (3,1))
#iloc targets columns im interested in, in this case, 
#take col 4 and 5
#-50: lastest 50 points
#:50 oldest 50 points