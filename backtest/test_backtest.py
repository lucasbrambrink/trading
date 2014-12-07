import os, django, sys
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()

from backtest import *
from models import Stocks,Prices
import csv

class CollectData:

	@staticmethod
	def market_snapshot_by_date(date):
		all_stocks = Prices.objects.filter(date=date)
		day = { 'date' : date, 'data' : all_stocks}
		return day

	@staticmethod
	def market_snapshot_by_stock(symbol):
		stock = Stocks.objects.get(symbol=symbol)
		all_prices = Prices.objects.filter(stock=stock)
		stock = { 'symbol' : symbol, 'data' : all_prices}
		return stock


class ParseDates:

	def __init__(self):
		self.all_dates = self.prepare_dates_for_data_collection()

	@staticmethod
	def prepare_dates_for_data_collection():
		all_dates = []
		for year in range(2000,2014):
			one_year = []
			for month in range(1,13):
				month_format = str(month)
				if month < 10:
					month_format = "0" + str(month)
				for day in range(1,32): ## it is okay for all months to go to 31 bc many of the dates wont be in the DB regardless (stock market closed)
					string = str(year) + "-" + str(month_format) + "-"
					if day < 10:
						string += "0" + str(day)
					else:
						string += str(day)
					all_dates.append(string)
		return all_dates

	@staticmethod
	def split_date_into_ints(date):
		year,month,day = date.split('-')
		year = int(year)
		if month[0] == '0':
			month = int(month[1])
		else:
			month = int(month)
		if day[0] == '0':
			day = int(day[1])
		else:
			day = int(day)
		return year,month,day

	def collect_dates_in_range(self,start_date,end_date):
		dates_in_range = []
		start_year,start_month,start_day = self.split_date_into_ints(start_date)
		end_year,end_month,end_day = self.split_date_into_ints(end_date)
		for date in self.prepare_dates_for_data_collection():
			year,month,day = self.split_date_into_ints(date)
			if year == start_year:
				if month >= start_month:
					dates_in_range.append(date)
			if start_year < year < end_year:
				dates_in_range.append(date)
			if year == end_year:
				if month <= end_month:
					dates_in_range.append(date) 
		return dates_in_range




class SampleAlgorithm:
## marks stocks whose 30 day SMA (simple moving average) has changed by more than 10%

	def __init__(self):
		self.initial_balance = 1000000
		self.start_date = '2010-01-01'
		self.end_date = '2011-01-01' ## let's just try one year for now

		## relevant dates ##
		self.dates_in_range = ParseDates().collect_dates_in_range(self.start_date,self.end_date)
		
		self.stocks_in_market = Stocks.objects.all()

		## calculator ##
		self.c = Calculator()


		## Sample Blocks ##
		self.sma_period = period
		self.percent_difference_to_buy = percent_difference_to_buy
		self.percent_difference_to_sell = percent_difference_to_sell

		## Ideas ##
		# - volatility of stock below certain threshold
		# - all other economic data can be used (P/E,R/E,...)
		# - covariance of sectors, industries --> aim for diversity in stocks
		# - covariance of stocks  to each other --> avoid holding on to similar covariances in portfolio
		#############

		## averages
		self.averages = self.get_simple_moving_averages()

		## stocks to buy!!
		self.stocks_to_buy = self.test_averages()


	def experience_time_period_with_algorithm(self):
		portfolio = []
		for date in self.dates_in_range:
			year,month,day = ParseDates.split_date_into_ints(date)
			if month > 2: ## range for days to go back
				if day == 1:
					all_stock_sma_pairs = self.get_sma_pair_previous_15_days(date)
					stocks_to_buy = []
					for pair in all_stock_sma_pairs:
						pd = self.c.percent_difference(pair,0,1,'sma')
						if pd > self.percent_difference_to_buy:
							stocks_to_buy.append(pair[0]['symbol'])

					## now you have all your stocks
					## rank their SMA's
					best_three = sorted(stocks_to_buy,'sma')[:3]
					



	@staticmethod
	def get_sma_pair_previous_15_days(date):
		all_stock_sma_pairs = []
		date_specific_index = self.dates_in_range.index(date)
		for stock in self.stocks_in_market:
			stock = Stocks.objects.get(symbol=stock_object.symbol)
			stock_prices_previous_15_days = []
			sma_pair = []
			count = 0
			for date in self.dates_in_range[date_specific_index:]: # effectively going backwards 15 days
				price = Prices.objects.filter(stock=stock).filter(date=date)
				if len(price) > 0:
					if len(stock_prices_previous_15_days) < 15: ## let's do a 15 day SMA
						stock_prices_previous_15_days.append({'price' : float(price[0].close) })
					else:
						sma = self.c.average(stock_prices_previous_15_days,'price')
						sma_pair.append({
							'symbol' : stock_object.symbol,
							'sma' : sma
							'date' : prices[-1].date
							})
						stock_prices_previous_15_days = []
						if len(sma_pair) == 2:
							all_stock_smas = (sma_pair[0],sma_pair[1],) ## tuples
							break


	def get_simple_moving_average(self):
		self.all_sma_averages = []
		for stock_object in self.stocks_in_market:
			stock = Stocks.objects.get(symbol=stock_object.symbol)
			prices = []
			for date in self.dates_in_range[::-1]:
				price = Prices.objects.filter(stock=stock).filter(date=date)
				if len(price) > 0:
					if len(prices) < 15: ## let's do a 15 day SMA
						prices.append({'price' : float(price[0].close) })
					else:
						sma = self.c.average(prices,'price')
						print(sma)
						averages.append({
							'symbol' : stock_object.symbol,
							'sma' : sma
							'date' : prices[-1].date
							})
						prices = []
		return averages

	def test_averages(self):
		stocks_to_buy = []
		for index,average in enumerate(self.averages):
			if index > 0:
				pc_change = round(((average['sma'] - self.averages[index-1]['sma']) / (self.averages[index-1]['sma'])),5)
				if pc_change > 0.10:
					stocks_to_buy.append(average)
		return stocks_to_buy

sa = SampleAlgorithm()
print(sa.stocks_to_buy)






