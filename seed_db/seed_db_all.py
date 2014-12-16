"""
This is the script for the purpose of importing data from csv files into database.
"""


import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
import django
django.setup()

from backtest.models import Stocks, Prices, TreasuryBill, Ratios

import csv

# CSV file storing all ticker symbols
ticker_csv = 'seed_db/csv_files/symbols.csv'

# CSV file storing all stock prices
prices_csv = 'seed_db/csv_files/prices.csv'
spy_csv = 'seed_db/csv_files/spy_prices.csv'
yield_csv = 'seed_db/csv_files/risk_free_yields.csv'

ratio_csv = 'seed_db/csv_files/ratios.csv'



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
    Seed prices table with Date, Open, High, Low, Close, Volume

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


def seed_stock_prices():
    """
    Seed prices table with Date, Open, High, Low, Close, Volume

    :return: Boolean. An indicator of whether seeding is successful or not.
    """
    with open(prices_csv, newline='') as prices:
        data_reader = csv.DictReader(prices, delimiter=',')
        # Read data
        current_stock = Stocks.objects.get(symbol='A')
        for row in data_reader:
            if row['Symbol'] != current_stock.symbol:
                current_stock = Stocks.objects.get(symbol=row['Symbol'])
                print(current_stock.symbol)
            Prices.objects.create(
                stock=current_stock,
                date=row['Date'],
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
                )
        print("Seeded Stocks successfully")
    return True

def seed_spy_prices():
    with open(spy_csv, newline='') as spy:
        data_reader = csv.DictReader(spy, delimiter=',')
        # Read data
        stock = Stocks.objects.create(
            name='SP 500 Market Index',
            sector='Index',
            industry='Market Index',
            symbol='SPY'
            )
        for row in data_reader:
            Prices.objects.create(
                stock=stock,
                date=row['Date'],
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
                )
        print("Seeded Spy successfully")

def seed_treasury_yield():
    """
    Seed Treasury Bill table with Date, 3 Month, 6 Month, 1 Year, 5 Year, 10 Year, 30 Year 

    :return: Boolean. An indicator of whether seeding is successful or not.
    """
    with open(yield_csv, newline='') as yields:
        data_reader = csv.DictReader(yields, delimiter=',')
        # Read data
        for row in data_reader:
            formatted_row = {
                'date': row['Date'],
                'three_month': row['3 Mo'],
                'six_month': row['6 Mo'],
                'one_year': row['1 Yr'],
                'five_year': row['5 Yr'],
                'ten_year': row['10 Yr'],
                'thirty_year': row['30 Yr']
            }
            for key in formatted_row:
                if formatted_row[key] == 'N/A':
                    formatted_row[key] = None
            TreasuryBill.objects.create(**formatted_row)  
        print('Seeded Treasury successfully!')
    return True


def seed_ratios():
    """
    Seed Valuation Ratios table with Date, cash per revenue, ev_ebitda, market_cap, current PE, rate of return 

    :return: Boolean. An indicator of whether seeding is successful or not.
    """
    with open(ratio_csv, newline='') as ratios:
        data_reader = csv.DictReader(ratios, delimiter=',')
        # Read data
        stock = Stocks.objects.get(symbol='A')
        for row in data_reader:
            if stock.symbol != row['Symbol']:
                stock = Stocks.objects.get(symbol=row['Symbol'])
            formatted_row = {
                'stock': stock,
                'date': row['Date'],
                'cash_revenue': row['CASH_REV'],
                'ev_ebitda': row['EV_EBITDA'],
                'market_cap': row['MKT_CAP'],
                'pe_current': row['PE_CURR'],
                'return_equity': row['ROE']
                }
            for key in formatted_row:
                if formatted_row[key] == "N/A":
                    formatted_row[key] = None
            Ratios.objects.create(**formatted_row)  
        print('Seeded ratios successfully!')
    return True


if __name__ == '__main__':
    # print(seed_stock_info())
    # print(seed_ratios())
    # print(seed_spy_prices())
    # print(seed_treasury_yield())
    # print(seed_stock_prices())

