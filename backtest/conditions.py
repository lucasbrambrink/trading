import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()

from calculator import *
from models import Stocks,Prices
import math
import re

class Conditions:

	def __init__(self,conditions,stocks_to_buy):
		self.conditions = conditions
		self.stocks_to_buy = stocks_to_buy

	def threshold_purge(self):
		## maybe mark them with strong negative points ? 
		for stock in self.stocks_to_buy:
            for key,value in self.conditions['threshold']['attributes']['price']:
                if ((key == 'below' and value > stock['price']) or
                    (key == 'above' and value < stock['price'])):
                    self.stocks_to_buy.remove(stock)
                    break

            if ((self.conditions['threshold']['attributes']['sector']['exclude'] != 'Null' and
            	stock['object'].sector in self.conditions['threshold']['attributes']['sector']['exclude']) or
                (self.conditions['threshold']['attributes']['sector']['include'] != 'Null' and
            	stock['object'].sector not in self.conditions['threshold']['attributes']['sector']['include'])):
                    self.stocks_to_buy.remove(stock)
                    break

            if ((self.conditions['threshold']['attributes']['industry']['exclude'] != 'Null' and
            	stock['object'].industry in self.conditions['threshold']['attributes']['industry']['exclude']) or
                (self.conditions['threshold']['attributes']['industry']['include'] != 'Null' and
            	stock['object'].industry not in self.conditions['threshold']['attributes']['industry']['include'])):
                    self.stocks_to_buy.remove(stock)
                    break
        return True
		
    def diversity_purge(self):
    	for stock in self.stocks_to_buy:
    		sector_count = len([1 for comparison in self.stocks_to_buy if stock.sector == comparison.sector]) 
			if sector_count > self.conditions['diversity']['attributes']['num_sector']:
				self.stocks_to_buy.remove(stock)
				break
			industry_count = len([1 for comparison in self.stocks_to_buy if stock.industry == comparison.industry])
			if industry_count > self.conditions['diversity']['attributes']['num_industry']:
				self.stocks_to_buy.remove(stock)
				break
		return True

	def crisis_purge(self):
		## crash --> all short term sma's plummet 
		## >> how do you analyze a crash? negative short term SMAs and increasing difference?
		short_sb = SMA_Block({'period' : 2})
		stocks_in_market = Stocks.objects.all()
		short_smas = [short_sb.get_sma_pair_per_stock(date,stock) for stock in stocks_in_market]
		number_of_declining_stocks = len([x for x in short_smas if x['sma_pair'][1] > x['sma_pair'][0]])
		percent_decline = number_of_declining_stocks / len(stocks_in_market)
		if percent_decline < self.crisis['attributes']['percent_decline']:
			if self.crisis['attributes']['behavior'] == 'hold':
				## do nothing
				continue
			if self.crisis['attributes']['behavior'] == 'sell':
				## sell all
				pass
		return True









