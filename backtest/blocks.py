import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()

from calculator import *
from models import Stocks,Prices
import math

class DB_Helper:

    @staticmethod
    def prices_in_range(period_identifier,stock_object,date):
        start_id = Prices.objects.filter(stock=stock_object).filter(date=date)[0].id
        end_id = start_id + (period_identifier) ## pair
        return Prices.objects.filter(id__range=(start_id,end_id))
        

class SMA_Block:
    
    def __init__(self,**kwargs):
        self.c = Calculator()
        for key in kwargs:
            setattr(self,key,kwargs[key])

    def get_sma_pair_per_stock(self,date,stock_object):
        sma1_prices,sma2_prices = [],[]
        prices_in_range = DB_Helper.prices_in_range((self.period*2),stock_object,date)
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

    def aggregate_stocks(self,date):
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

    def get_volatility_per_stock(self,stock_object,date):
        prices_in_range = DB_Helper.prices_in_range(self.period,stock_object,date)
        price_objects = [{'price' : float(x.close)} for x in prices_in_range]
        volatility = Calculator.stdev(price_objects,'price')
        return {
            'object' : stock_object,
            'volatility' : volatility,
            'price' : price_objects[-1]['price'],
            'symbol' : stock_object.symbol
        }


    def aggregate_stocks(self,date):
        all_volatilities = [get_volatility_per_stock(stock_object,date) for stock_object in self.stocks_in_market]
        return [volatility for volatility in all_volatilities if volatility['volatility'] > self.threshold_to_buy]

class Covariance_Block:

    def __init__(self,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])

    def get_covariance_per_stock(self,stock_object,date):
        prices_in_range = DB_Helper.prices_in_range(self.period,stock_object,date)
        price_objects = [{'price' : float(x.close)} for x in prices_in_range]
        covariance = Calculator.covariance(price_objects,self.benchmark,'price')
        return {
            'object' : stock_object,
            'covariance' : covariance,
            'price' : price_objects[-1]['price'],
            'symbol' : stock_object.symbol
        }

    def aggregate_stocks(self,date):
        self.benchmark = Prices.objects.filter(stock=)





