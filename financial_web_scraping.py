# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 15:41:26 2020

@author: Austin
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["AAPL", "MSFT"]
financial_dir = {}

for ticker in tickers:
    temp_dir = {}
    url = 'https://hk.finance.yahoo.com/quote/'+ticker+'/balance-sheet?p='+ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" :"rw-expanded"})
        for row in rows:
            temp_dir[row.get_text(seperator= '|').split("|")[0]] = row.get_text(seperator='|').split("|")[1]
            #populate temp_dir
            #seperator adds a seprator lol...then split the data into a list .split("|") then take first two elemnts of list[0:2]
    url = 'https://hk.finance.yahoo.com/quote/' + ticker + '/financials?p=' +ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" :"rw-expanded"})
        for row in rows:
            temp_dir[row.get_text(seperator= '|').split("|")[0]] = row.get_text(seperator='|').split("|")[1]
    url = 'https://hk.finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' +ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" :"rw-expanded"})
        for row in rows:
            temp_dir[row.get_text(seperator= '|').split("|")[0]] = row.get_text(seperator='|').split("|")[1]
    url = 'https://hk.finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' +ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("table", {"class": "W(100%) Bdcl(c) Mt(10px) "})
    for t in tabl:
        rows = t.find_all("tr")
        for row in rows:
            temp_dir[row.get_text(seperator= '|').split("|")[0]] = row.get_text(seperator='|').split("|")[1]
    financial_dir[ticker] = temp_dir
    
combined_financials = pd.DataFrame(financial_dir)
tickers = combined_financials.columns
for ticker in tickers:
    combined_financials = combined_financials[~combined_financials[ticker].str.contains["[a-z]"].fillna(False)] #remove extraneous rows