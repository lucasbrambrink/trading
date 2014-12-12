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
			for key,value in self.conditions['threshold']['price']:
				if [(key == 'below' and value > stock['price']) or
				 (key == 'above' and value < stock['price'])]:
					self.stocks_to_buy.remove(stock)
					break

			if ((stock['object'].sector in self.conditions['threshold']['sector']['exclude']) or
            	(stock['object'].sector not in self.conditions['threshold']['sector']['include'])):
					self.stocks_to_buy.remove(stock)
					break

			if ((stock['object'].industry in self.conditions['threshold']['industry']['exclude']) or
                (stock['object'].industry not in self.conditions['threshold']['industry']['include'])):
					self.stocks_to_buy.remove(stock)
					break
		return True

	def diversity_purge(self):
		for stock in self.stocks_to_buy:
			sector_count = len([1 for comparison in self.stocks_to_buy if stock.sector == comparison.sector]) 
			if sector_count > self.conditions['diversity']['num_sector']:
				self.stocks_to_buy.remove(stock)
				break
			industry_count = len([1 for comparison in self.stocks_to_buy if stock.industry == comparison.industry])
			if industry_count > self.conditions['diversity']['num_industry']:
				self.stocks_to_buy.remove(stock)
				break
		return True

	def aggregate_survivors(self):
		for condition in self.conditions:
			if condition == 'threshold':
				self.threshold_purge()
			if condition == 'diversity':
				self.diversity_purge()
			if conditions == 'crisis':
				self.test_crisis_event()
		return self.stocks_to_buy


	def test_crisis_event(self):
		## crash --> all short term sma's plummet 
		## >> how do you analyze a crash? negative short term SMAs and increasing difference?
		short_sb = SMA_Block({'period' : 2})
		stocks_in_market = Stocks.objects.all()
		short_smas = [short_sb.get_sma_pair_per_stock(date,stock) for stock in stocks_in_market]
		number_of_declining_stocks = len([x for x in short_smas if x['sma_pair'][1] > x['sma_pair'][0]])
		percent_decline = number_of_declining_stocks / len(stocks_in_market)
		if percent_decline < self.conditions['crisis']['percent_decline']:
			if self.conditions['crisis']['behavior'] == 'hold':
				## do nothing
				pass
			if self.conditions['crisis']['behavior'] == 'sell':
				## sell all
				pass
		return True









