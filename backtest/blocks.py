import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()

from calculator import *
from models import Stocks,Prices
import math
from datetime import date,timedelta

class DB_Helper:

    @staticmethod
    def prices_in_range(period1_identifier,period2_identifier,stock_object,date):
        start_date = date - timedelta(days=(period1_identifier + period2_identifier))
        return list(Prices.objects.filter(stock=stock_object).filter(date__range=(start_date,date)).order_by('date'))
        

class SMA_Block:
    
    def __init__(self,**kwargs):
        self.c = Calculator()
        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    def get_sma_pair_per_stock(self,date,stock_object):
        sma1_prices,sma2_prices = [],[]
        prices_in_range = DB_Helper.prices_in_range(self.period1,self.period2,stock_object,date)
        if len(prices_in_range) == 0:
            return None
        for index,price in enumerate(prices_in_range[::-1]): ## arrange into proper order
            price = {'price': float(prices_in_range[index].close), 'date' : date}
            if index < self.period1:
                sma1_prices.append(price)
            else:
                sma2_prices.append(price)
        sma1 = self.c.average(sma1_prices,'price')
        sma2 = self.c.average(sma2_prices,'price')
        sma_pair = {
            'symbol' : stock_object.symbol,
            'sma_pair' : (sma1,sma2,),
            'date' : date,
            'todays_price' : prices_in_range[-1].close,
            'todays_volume': prices_in_range[-1].volume,
            'object' : stock_object
            }
        return sma_pair

    def aggregate_stocks(self,stocks,date):
        stocks_to_buy = []
        all_stock_sma_pairs = [self.get_sma_pair_per_stock(date,stock_object) for stock_object in stocks]
        for pair in all_stock_sma_pairs:
            if pair is not None:
                pd = self.c.percent_change_simple(pair['sma_pair'][1],pair['sma_pair'][0])
                if pd > self.percent_difference_to_buy:
                    stocks_to_buy.append({
                        'symbol': pair['symbol'],
                        'sma_score': self.appetite*pd,
                        'todays_price': pair['todays_price'],
                        'todays_volume': pair['todays_volume'],
                        'object': pair['object'],
                        })
        return stocks_to_buy


class Volatility_Block:

    def __init__(self,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])
        
    def get_volatility_per_stock(self,stock_object,date):
        prices_in_range = DB_Helper.prices_in_range(self.period,0,stock_object,date)
        price_objects = [{'price' : x.close} for x in prices_in_range]
        if len(price_objects) == 0:
            return None
        volatility = Calculator.stdev(price_objects,'price')
        vol_percentage = round((volatility/prices_in_range[-1].close),4)
        return {
            'object': stock_object,
            'vol_percentage': vol_percentage,
            'volatility_score': self.appetite*volatility,
            'symbol': stock_object.symbol,
            'todays_price' : prices_in_range[-1].close,
            'todays_volume': prices_in_range[-1].volume,
        }

    def aggregate_stocks(self,stocks,date):
        all_volatilities = [self.get_volatility_per_stock(stock_object,date) for stock_object in stocks]
        return [x for x in all_volatilities if x is not None and self.range[0] < x['vol_percentage'] < self.range[1]]

class Covariance_Block:

    def __init__(self,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])
    
    def get_covariance_per_stock(self,stock_object,date):
        prices_in_range = DB_Helper.prices_in_range(self.period,0,stock_object,date)
        price_objects = [{'price' : x.close} for x in prices_in_range]
        if len(price_objects) == 0:
            return None
        covariance = Calculator.covariance(price_objects,self.benchmark_prices,'price')
        return {
            'object': stock_object,
            'covariance' : covariance,
            'covariance_score': self.appetite*covariance,
            'symbol': stock_object.symbol,
            'todays_price' : prices_in_range[-1].close,
            'todays_volume': prices_in_range[-1].volume
        }

    def parse_benchmark(self,date):
        benchmark = Stocks.objects.get(symbol=self.benchmark)
        prices = DB_Helper.prices_in_range(self.period,0,benchmark,date)
        return [{'price' : x.close} for x in prices]

    def aggregate_stocks(self,stocks,date):
        self.benchmark_prices = self.parse_benchmark(date)
        all_covariances = [self.get_covariance_per_stock(stock_object,date) for stock_object in stocks]
        return [c for c in all_covariances if c is not None and self.range[0] < c['covariance'] < self.range[1]]





