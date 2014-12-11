## Scraper for all Stock Data for Final Project ##
import csv
import requests

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
import django
django.setup()

from backtest.models import Stocks,Prices

def get_price(symbol):
    base_url = 'https://www.quandl.com/api/v1/datasets/WIKI/'
    auth_token='HdD4E3ee682f2C4mJg11'
    start_day = '2000-01-01'
    end_day = '2014-12-01'
    query_str = base_url + "{}.json?trim_start={}&trim_end{}&auth_token={}".format(symbol, start_day, end_day, auth_token)
    response = requests.get(query_str, headers={'content-type': 'application/json'})
    for x in range(5):
        try:
            r = response.json()
            return r
        except:
            response = requests.get(query_str, headers={'content-type': 'application/json'}) 
    return None


'''
    {"urlize_name":"Monsanto-Company-MON-Prices-Dividends-Splits-and-Trading-Volume",
    "data": [
    $"Date","Open","High","Low","Close","Volume"$
    ["2014-11-12",118.25,119.487,117.79,118.99, ...]
    ["2014-11-11",116.7,118.36,116.7,118.31,...]
    ]}
'''

def create_the_entire_db():
    all_stocks = Stocks.objects.all()
    stock_prices = csv.writer(open('stock_prices_v3.csv', 'w', newline=''))

    # Read data
    for stock in all_stocks:
        prices = get_price(stock.symbol)
        for key in prices: ## this is only to avoid a key error if Quandl throws an error, for continuity
            if key == 'data':
                print(stock.symbol)
                for data_point in prices['data']:
                    ## symbol, date, open, high, low, close
                    # Prices.objects.create(stock=stock,date=data_point[0],open=data_point[1],high=data_point[2],low=data_point[3],close=data_point[4],volume=data_point[5])
                    stock_prices.writerow((stock.symbol,data_point[0],data_point[1],data_point[2],data_point[3],data_point[4],data_point[5]))

    print('seeded stocks')
    return True

def find_errors():
    rows = csv.reader(open('stock_prices_v3.csv',newline=''))
    for row in rows:
        if len(row) != 7:
            print(row.line_num)
        if 'null' in row:
            print(rows.line_num)
    return "Done"



## Script ##
# create_the_entire_db()
find_errors()
print("All is well! Success!")