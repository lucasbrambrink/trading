import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
import django
django.setup()

from backtest.models import Stocks, Prices

import csv

# CSV file storing all stock prices
prices_csv = 'spy_no_errors.csv'

def fix_errors():
    prices_file = csv.DictReader(open(prices_csv, newline=''),delimiter=',')
    new_file = csv.writer(open('spy_no_errors.csv','w',newline=''))
    previous_row = {'Date': '2000-01-01'}
    for row in prices_file:
        if row['Open'] is None or row['High'] is None or row['Low'] is None or row['Close'] is None or row['Volume'] is None:
            new_file.writerow([
                row['Date'],
                previous_row['Open'],
                previous_row['High'],
                previous_row['Low'],
                previous_row['Close'],
                previous_row['Volume']
                ])
        else:
            new_file.writerow([
                row['Date'],
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume']
                ])
        previous_row = row

def add_spy_prices_info():
    prices_file = csv.DictReader(open(prices_csv, newline=''),delimiter=',')
    spy = Stocks.objects.get(symbol='SPY')
    for row in prices_file:
        Prices.objects.create(
            stock=spy,
            date=row['Date'],
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            volume=row['Volume']
            )
    return "Seeded Successfully"


if __name__ == '__main__':
    # fix_errors()
    print(add_spy_prices_info())