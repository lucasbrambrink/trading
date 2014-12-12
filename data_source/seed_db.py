"""
This is the script for the purpose of importing data from csv files into database.
"""


import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
import django
django.setup()

from backtest.models import Stocks, Prices

import csv

# CSV file storing all stock prices
prices_csv = './csv/prices_no_errors.csv'

# Valid ticker list
ticker_csv = './csv/ticker-list.csv'

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
                try:
                    Stocks.objects.get(symbol=row['Name'])
                except Stocks.DoesNotExist:
                    Stocks.objects.create(name=row['Name'], sector=row['Sector'], industry=row['Industry'],
                                      symbol=row['Ticker'])

            print('Finish seeding stock information.')
            return True
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        return False

def seed_stock_price(limit):
    """
    Seed prices table with Date, Open, High, Low, Close

    :return: Boolean. An indicator of whether seeding is successful or not.
    """

    # Check if it contains data
    try:
        Prices.objects.get(pk=1000000)
        ans = input('It seems there are 1000000 data inside, do you still want to seed the table? Y/N\n')
        if ans != 'Y':
            print('Abort seeding!')
    except Prices.DoesNotExist:
        # There is no data
        pass

    count = 0
    stock = Stocks.objects.get(pk=1)
    try:
        with open(prices_csv, newline='') as prices_f:
            data_reader = csv.reader(prices_f, delimiter=',')
            # Skip fieldnames
            next(data_reader)

            # Read data
            while count < limit:
                row = next(data_reader)
                if row[0] != stock.symbol:
                    # New stock
                    try:
                        stock = Stocks.objects.get(symbol=row[0])
                    except Stocks.DoesNotExist:
                        stock = None

                elif stock is not None:
                    # price row and stock is valid
                    try:
                        Prices.objects.create(stock=stock, date=row[1], open=row[2], high=row[3],
                                              low=row[4], close=row[5], volume=row[6])
                        count += 1
                    except Exception:
                        print("Unexpected error:", sys.exc_info())

            print('Finish seeding stock prices.')
            return True
    except Exception:
        print("Unexpected error:", sys.exc_info())
        return False


if __name__ == '__main__':
    print(seed_stock_info())
    print(seed_stock_price(10000))
