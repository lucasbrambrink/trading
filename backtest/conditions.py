from .calculator import *
from .models import Stocks,Prices
import math
import re

class Conditions:

	def __init__(self,conditions,stocks_to_buy):
		self.conditions = conditions
		self.stocks_to_buy = stocks_to_buy

	def threshold_purge(self):
		survivors = []
		for stock in self.stocks_to_buy:
			if 'price' in self.conditions['thresholds']:
				if 'above' in self.conditions['thresholds']['price']:
					if stock['todays_price'] < self.conditions['thresholds']['price']['above']:
						continue
				if 'below' in self.conditions['thresholds']['price']:
					if stock['todays_price'] > self.conditions['thresholds']['price']['below']:
						continue

			if 'sector' in self.conditions['thresholds']:
				if 'exclude' in self.conditions['thresholds']['sector']:
					if stock['object'].sector in self.conditions['thresholds']['sector']['exclude']:
						continue
				if 'include' in self.conditions['thresholds']['sector']:
					if stock['object'].sector not in self.conditions['thresholds']['sector']['include']:
						continue

			if 'industry' in self.conditions['thresholds']:
				if 'exclude' in self.conditions['thresholds']['industry']:
					if stock['object'].industry in self.conditions['thresholds']['industry']['exclude']:
						continue
				if 'include' in self.conditions['thresholds']['industry']:
					if stock['object'].industry not in self.conditions['thresholds']['industry']['include']:
						continue

			survivors.append(stock)
		return survivors

	def diversity_purge(self):
		survivors = []
		for stock in sorted(self.stocks_to_buy,key=lambda x: x['agg_score'],reverse=True):
			for key in self.conditions['diversity']:
				current_count = len([1 for comparison in survivors if getattr(stock['object'],key[4:]) == getattr(comparison['object'],key[4:])])
				if current_count > self.conditions['diversity'][key]:
					continue
			survivors.append(stock)
		return survivors

	def aggregate_survivors(self):
		for condition in self.conditions:
			if condition == 'thresholds':
				self.stocks_to_buy = self.threshold_purge()
			if condition == 'diversity':
				self.stocks_to_buy = self.diversity_purge()
			if condition == 'crisis':
				self.stocks_to_buy = self.test_crisis_event()
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









