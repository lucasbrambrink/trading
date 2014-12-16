"""
This script is for purpose of fetching stock's fundamental indicators and financial ratios from Damodaran
Financial Data database via Quandl
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
import django
django.setup()

from backtest.models import Stocks

import requests

# Ratios to get
ratios = ['CASH_REV','EV_EBITDA','MKT_CAP','PE_CURR','ROE']

# API base url
base_url = 'https://www.quandl.com/api/v1/datasets/DMDRN/'

def fetch(ticker, name, start, end):
    """
    This method will fetch a annually recorded indicators or ratios with its name for a stock with its
    ticker within a period of time from start year to end year

    :param ticker: stock ticker symbol
    :param name: indicator or ratio name
    :param start: start year
    :param end: end year
    :return: A list of lists of [date, ratio]
    """
    query_str = '{ticker}_{name}.json?trim_start={start_year}-12-31&trim_end={end_year}-12-31&auth_token={auth_token}'\
        .format(ticker=ticker, name=name, start_year=start, end_year=end, auth_token='HdD4E3ee682f2C4mJg11')
    response = requests.get(base_url + query_str).json()
    try:
        return response['data']
    except KeyError:
        return []

import csv
def fetch_all_stocks(ratios):
    all_stocks = Stocks.objects.all()
    data = csv.writer(open('ratios.csv','w',newline=''))
    for index,stock in enumerate(all_stocks):
        print(stock.symbol)
        fin_ratios = []
        for ratio in ratios:
            fin_ratios.append({ratio: fetch(stock.symbol,ratio,'2000','2014')})
        formatted_ratios = {}
        for ratio in fin_ratios:
            for key in ratio:
                for date in ratio[key]:
                    try:
                        formatted_ratios[date[0]][key] = date[1]
                    except KeyError:
                        formatted_ratios[date[0]] = {key: date[1]}
        for key in formatted_ratios:
            row = [str(stock.symbol),str(key)]
            for set_key in ratios:
                try:
                    row.append(round(formatted_ratios[key][set_key],5))
                except KeyError:
                    row.append('N/A')
            data.writerow(row)


fetch_all_stocks(ratios)