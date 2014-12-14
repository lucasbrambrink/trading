import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()

from calculator import *
from models import Stocks,Prices
import math
import re

class Conditions:

	def __init__(self,conditions,stocks):
		self.conditions = conditions
		self.stocks = stocks

	def threshold_purge(self):
		for stock in self.stocks[:]:
			if 'price' in self.conditions['thresholds']:
				if 'above' in self.conditions['thresholds']['price']:
					if stock['todays_price'] < self.conditions['thresholds']['price']['above']:
						self.stocks.remove(stock)
						continue
				if 'below' in self.conditions['thresholds']['price']:
					if stock['todays_price'] > self.conditions['thresholds']['price']['below']:
						self.stocks.remove(stock)
						continue

			if 'sector' in self.conditions['thresholds']:
				if 'exclude' in self.conditions['thresholds']['sector']:
					if stock['object'].sector in self.conditions['thresholds']['sector']['exclude']:
						self.stocks.remove(stock)
						continue
				if 'include' in self.conditions['thresholds']['sector']:
					if stock['object'].sector not in self.conditions['thresholds']['sector']['include']:
						self.stocks.remove(stock)
						continue

			if 'industry' in self.conditions['thresholds']:
				if 'exclude' in self.conditions['thresholds']['industry']:
					if stock['object'].industry in self.conditions['thresholds']['industry']['exclude']:
						self.stocks.remove(stock)
						continue
				if 'include' in self.conditions['thresholds']['industry']:
					if stock['object'].industry not in self.conditions['thresholds']['industry']['include']:
						self.stocks.remove(stock)
						continue

		return True

	def diversity_purge(self):
		for stock in sorted(self.stocks,key=lambda x: x['agg_score'],reverse=True)[:]:
			for condition in self.conditions['diversity']:
				for key in condition:
					if key != 'behavior':
						current_count = len([1 for comparison in self.stocks if getattr(stock['object'],key[4:]) == getattr(comparison['object'],key[4:])])
						if current_count > condition[key]:
							self.stocks.remove(stock)
		return True

	def aggregate_survivors(self):
		for condition in self.conditions:
			if condition == 'thresholds':
				self.threshold_purge()
			if condition == 'diversity':
				self.diversity_purge()
			if condition == 'crisis':
				self.test_crisis_event()
		return self.stocks


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









