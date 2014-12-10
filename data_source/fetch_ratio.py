"""
This script is for purpose of fetching stock's fundamental indicators and financial ratios from Damodaran
Financial Data database via Quandl
"""


import requests


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
    query_str = '{ticker}_{name}.json?trim_start={start_year}-12-31&trim_end={end_year}-12-31'\
        .format(ticker=ticker, name=name, start_year=start, end_year=end)
    response = requests.get(base_url + query_str).json()

    return response['data']