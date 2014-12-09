"""
This is the script for the purpose of importing data from csv files into database.
"""


import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
import django
django.setup()
from django.db.models import ObjectDoesNotExist

from backtest.models import Stocks, Prices

import csv

# CSV file storing all stock prices
prices_csv = './csv/stock_prices.csv'

# Valid ticker list
ticker_csv = './csv/valid-ticker-list.csv'

def seed_stock_info():
    """
    Seed stocks table with Name, Sector, Industry, Ticker

    :return: Boolean. An indicator of whether seeding is successful or not.
    """

    try:
        with open(ticker_csv, newline='') as ticker_f:
            data_reader = csv.DictReader(ticker_f, delimiter=',')

            # Read data
            for row in data_reader:
                Stocks.objects.create(name=row['Name'], sector=row['Sector'], industry=row['Industry'],
                                      ticker=row['Ticker'])

            print('Finish seeding stock information.')
            return True
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        return False

def seed_stock_price():
    """
    Seed prices table with Date, Open, High, Low, Close

    :return: Boolean. An indicator of whether seeding is successful or not.
    """

    # Check if it contains data
    try:
        price = Prices.objects.get(pk=1000000)
        ans = input('It seems there are 1000000 data inside, do you still want to seed the table? Y/N\n')
        if ans != 'Y':
            print('Abort seeding!')
    except:
        # There is no data
        pass

    try:
        with open(prices_csv, newline='') as prices_f:
            data_reader = csv.reader(prices_f, delimiter=',')

            # Read data
            for row in data_reader:
                if len(row) != 6:
                    # Info row
                    try:
                        stock = Stocks.objects.get(ticker=row[0])
                    except ObjectDoesNotExist:
                        stock = None

                elif stock is not None:
                    # price row and stock is valid
                    Prices.objects.create(stock=stock, date=row[1], open=row[2], high=row[3], low=row[4], close=row[5])

            print('Finish seeding stock prices.')
            return True
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        return False


if __name__ == '__main__':
    print(seed_stock_info())
    print(seed_stock_price())
