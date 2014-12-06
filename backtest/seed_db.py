
import os, django, sys
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()

from models import Stocks,Prices

import csv

csv_file = '../csv_files/stock_prices.csv'

if __name__ == '__main__':

    with open(csv_file,'r') as stock_data:
            data = csv.reader(stock_data)
            for date in data:
                if date[1][0].isalpha():
                    stock = {
                        'symbol' : date[0],
                        'name' : date[1],
                        'sector' : date[2],
                        'industry' : date[3]
                    }
                    stock = Stocks.objects.create(**stock)
                if date[1][0] == '2':
                    stock_price = {
                        'date' : date[1],
                        'open' : date[2],
                        'high' : date[3],
                        'low' : date[4],
                        'close' : date[5]
                    }
                    Prices.objects.create(stock=stock, **stock_price)
    print("Seeding Complete")
