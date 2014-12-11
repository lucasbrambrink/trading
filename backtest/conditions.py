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