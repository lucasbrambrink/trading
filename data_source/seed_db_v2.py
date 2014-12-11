import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
import django
django.setup()
from django.db.models import ObjectDoesNotExist

from backtest.models import Stocks, Prices

import csv

# CSV file storing all stock prices
prices_csv = 'prices_no_errors.csv'

def check_for_errors():
    prices_file = csv.DictReader(open(prices_csv, newline=''),delimiter=',')
    for row in prices_file:
        if row['Date'] == '' or len(row['Date']) != 10 or row['Open'] == '' or row['High'] == '' or row['Low'] == '' or row['Close'] == '' or row['Volume'] == '':
            print(row)

def fix_errors():
    prices_file = csv.DictReader(open(prices_csv, newline=''),delimiter=',')
    new_file = csv.writer(open('prices_no_errors.csv','w',newline=''))
    previous_row = {'Date': '2000-01-01'}
    for row in prices_file:
        if row['Open'] == '' or row['High'] == '' or row['Low'] == '' or row['Close'] == '' or row['Volume'] == '':
            new_file.writerow([
                previous_row['Symbol'],
                row['Date'],
                previous_row['Open'],
                previous_row['High'],
                previous_row['Low'],
                previous_row['Close'],
                previous_row['Volume']
                ])
        else:
            new_file.writerow([
                row['Symbol'],
                row['Date'],
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume']
                ])
        previous_row = row
    

def add_prices_info():
    prices_file = csv.DictReader(open(prices_csv, newline=''),delimiter=',')
    first_symbol = prices_file.__next__()
    current_symbol = first_symbol['Symbol']
    current_stock = Stocks.objects.get(symbol=current_symbol)
    for row in prices_file:
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
    return "Seeded Successfully"


if __name__ == '__main__':
    # check_for_errors()
    # fix_errors()
    print(add_prices_info())
