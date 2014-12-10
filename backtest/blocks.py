import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()

from calculator import *
from models import Stocks,Prices
import math


class SMA_Block:
    
    def __init__(self,**kwargs):
        self.c = Calculator()
        for key in kwargs:
            setattr(self,key,kwargs[key])

        self.recommendations = self.aggregate_stocks()

    def get_sma_pair_per_stock(self,date,stock_object):
        sma1_prices = []
        sma2_prices = []
        start_id = Prices.objects.filter(stock=stock_object).filter(date=date)
        ## DB is seeded backwards (starts with latest date)
        end_id = start_id + (self.sma_period * 2) ## pair
        prices_in_range = Prices.objects.filter(id__range=(start_id,end_id))
        for index,price in enumerate(prices_in_range[::-1]): ## arrange into proper order
            if len(prices_in_range[index].close) == 0:
                continue 
            price = {'price': float(prices_in_range[index].close), 'date' : date}
            if index < (len(prices_in_range)/2):
                sma1_prices.append(price)
            else:
                sma2_prices.append(price)
        sma1 = self.c.average(sma1_prices,'price')
        sma2 = self.c.average(sma2_prices,'price')
        sma_pair = {
            'symbol' : stock_object.symbol,
            'sma_pair' : (sma1,sma2,),
            'date' : date,
            'close' : prices_in_range[0].close,
            'object' : stock_object
            }
        return sma_pair

    def aggregate_stocks(self):
        stocks_to_buy = []
        all_stock_sma_pairs = [self.get_sma_pair_per_stock(date,stock_object) for stock_object in self.stocks_in_market]
        for pair in all_stock_sma_pairs:
            pd = self.c.percent_change_simple(pair['sma_pair'][1],pair['sma_pair'][0])
            if pd > self.sma_percent_difference_to_buy:
                stocks_to_buy.append({
                    'symbol' : pair['symbol'],
                    'sma_dif' : pd,
                    'price' : pair['close'],
                    'object' : pair['object']
                    })
        return stocks_to_buy


class Volatility_Block:

    def __init__(self,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])

    def get_volatility_per_stock(self):
        pass

    def aggregate_stocks(self):

