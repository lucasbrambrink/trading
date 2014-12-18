"""
This is the script for the purpose of importing data from csv files into database.
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
import django
django.setup()

from backtest.models import Stocks, Prices

import csv

# CSV file with treasury yields
yield_csv = 'yields_with_dates.csv'

def fix_errors():
    yields = csv.DictReader(open(yield_csv, newline=''),delimiter=',')
    new_file = csv.writer(open('yields_with_dates.csv','w',newline=''))
    for row in yields:
        if row['Date'][-2] == '9':
            year = '19' + str(row['Date'][-2:])
        else:
            year = '20' + str(row['Date'][-2:])
        formatted_date = year +'-'+ str(row['Date'])[0:2]+'-'+str(row['Date'])[3:5]
        # print(formatted_date)
        new_file.writerow([
            formatted_date,
            row['1 Mo'],
            row['3 Mo'],
            row['6 Mo'],
            row['1 Yr'],
            row['2 Yr'],
            row['3 Yr'],
            row['5 Yr'],
            row['7 Yr'],
            row['10 Yr'],
            row['20 Yr'],
            row['30 Yr'],
            ])
        # else:
        #     new_file.writerow([
        #         row['Symbol'],
        #         row['Date'],
        #         row['Open'],
        #         row['High'],
        #         row['Low'],
        #         row['Close'],
        #         row['Volume']
        #         ])
        # previous_row = row

def seed_yield_info():
    stock = Stocks.objects.filter(symbol='RFTB')
    if len(stock) == 0:
        stock = Stocks.objects.create(symbol='RFTB',industry='Treasury',sector='Treasury',name='Risk Free One Year Treasury Bill Yields')
    else:
        stock = stock[0]
    with open(yield_csv, newline='') as yields:
        data_reader = csv.DictReader(yields, delimiter=',')
        ## delete prices before seeding ##
        all_prices = Prices.objects.filter(stock=stock)
        for price in all_prices:
            price.delete()
        # Read data
        for row in data_reader:
            if row['3 Mo'] == 'N/A' or row['6 Mo'] == 'N/A' or row['1 Yr'] == 'N/A' or row['5 Yr'] == 'N/A' or row['10 Yr'] == 'N/A':
                print(row)
            Prices.objects.create(
                stock=stock,
                date=row['Date'],
                open=row['3 Mo'],
                high=row['6 Mo'],
                low=row['1 Yr'],
                close=row['5 Yr'],
                volume=row['10 Yr']
            )  
        print('seeded successfully!')





if __name__ == '__main__':
    # print(fix_errors())
    print(seed_yield_info())
