## set up django
import os, django, sys
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()


## get contingencies
from calculator import *
from models import Stocks,Prices
import csv
import math



## Helper Class
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

## Helper Class
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


class BacktestingEnvironment:

	def __init__(self,start_date,end_date,initial_balance):
		self.start_date = start_date
		self.end_date = end_date

		## relevant dates ##
		self.dates_in_range = ParseDates().collect_dates_in_range(self.start_date,self.end_date)
		
		## initialize stocks ##
		self.stocks_in_market = Stocks.objects.all()

		## calculators ##
		self.c = Calculator()
		self.pc = PortfolioCalculator()

		## initialize portfolio ##
		self.portfolio = []
		self.initial_balance = initial_balance
		self.balance = initial_balance


	## main backtesting method ##
	def run_period_with_algorithm(self):
		print('run algorithm')
		portfolio = []
		index = 0
		while index < len(self.dates_in_range):
			date = self.dates_in_range[index]
			year,month,day = ParseDates.split_date_into_ints(date)
			if month > 2: ## range for days to go back
				if day < 5:
					## test if it's a proper trading day
					sample = Prices.objects.filter(date=date)
					if len(sample) == 0:
						index += 1
					else:
						## wont repeat more than once
						self.execute_trading_session(date)
						self.print_information(date)
						index += 15 ## ensures if condition won't be met twice per month
			index += 1
		return True

	## helper method ##
	def execute_trading_session(self,date):
		print('executing trading session, date: ',date)
		stocks_to_buy = self.find_stocks_to_buy(date)

		## sell everything in portfolio first ( just do it )
		for asset in self.portfolio:
			self.sell_stock(asset['symbol'],date)

		## now buy stocks 
		## rank their SMA pd's
		best_three = sorted(stocks_to_buy,key=(lambda x: x['pd']),reverse=True)[:3]
		## equally divide holdings to all three
		investment_per_stock = math.floor(self.balance / 3)
		for stock in best_three:
			self.buy_stock(investment_per_stock,stock['symbol'],date)
		return True

	## support methods ##
	def buy_stock(self,dollar_amount,symbol,date):
		stock = Stocks.objects.get(symbol=symbol)
		price = Prices.objects.filter(stock=stock).filter(date=date)
		if len(price) > 0:
			quantity = math.floor(dollar_amount / float(price[0].close))
			self.balance -= dollar_amount
			self.portfolio.append({
				'symbol' : stock.symbol,
				'price_purchased' : float(price[0].close),
				'quantity' : quantity
				})
			return True
		else:
			return False # unable to buy for this date

	def sell_stock(self,symbol,date):
		stock = Stocks.objects.get(symbol=symbol)
		price = Prices.objects.filter(stock=stock).filter(date=date)
		if len(price) > 0:
			for asset in self.portfolio:
				if asset['symbol'] == symbol:
					sale = round((asset['quantity']*float(price[0].close)),2)
					self.balance += sale
					self.portfolio.remove(asset)
			return True
		else:
			return False

	def get_sma_pair_previous_2_periods(self,date):
		print('get previous 2 smas')
		all_stock_sma_pairs = []
		date_specific_index = self.dates_in_range.index(date)
		for stock_object in self.stocks_in_market:
			stock_prices_previous_period = []
			sma_pair = []
			count = 0
			for date in self.dates_in_range[date_specific_index::-1]: # effectively going backwards 15 days
				price = Prices.objects.filter(stock=stock_object).filter(date=date)
				if len(price) > 0:
					if len(stock_prices_previous_period) < self.sma_period: ## let's do a 15 day SMA
						stock_prices_previous_period.append({'price' : float(price[0].close),'date' : date })
					else:
						sma = self.c.average(stock_prices_previous_period,'price')
						sma_pair.append({
							'symbol' : stock_object.symbol,
							'sma' : sma,
							'date' : stock_prices_previous_period[-1]['date'],
							})
						stock_prices_previous_period = []
						if len(sma_pair) == 2:
							all_stock_sma_pairs.append((sma_pair[0],sma_pair[1],)) ## tuples
							break
		return all_stock_sma_pairs


	def find_stocks_to_buy(self,date):
		print('determining stocks to match sma threshold')
		all_stock_sma_pairs = self.get_sma_pair_previous_2_periods(date)
		stocks_to_buy = []
		for pair in all_stock_sma_pairs:
			pd = self.c.percent_change(pair,0,1,'sma')
			if pd > self.percent_difference_to_buy:
				stocks_to_buy.append({
					'symbol' : pair[0]['symbol'],
					'pd' : pd
					})
		return stocks_to_buy

	## Views ##
	def print_information(self,date):
		print("------------------------------------------------")
		print("Date : ",date)
		for asset in self.portfolio:
			line = "Stock : " + asset['symbol'] + ', quantity : ' + str(asset['quantity']) + ', at : ' + str(asset['price_purchased'])
			print(line)
		print("Balance : ",round(self.balance,2))
		value = round(PortfolioCalculator(self.portfolio).value,2)
		print("Portfolio Value : ",value)
		returns = round(float(((self.balance + value) - 1000000) / 1000000),2)
		print("Returns : ",returns)
		return True


## Algorithms built from Blocks ##

class SampleAlgorithm:
## marks stocks whose 30 day SMA (simple moving average) has changed by more than 10%

	def __init__(self,period,percent_difference_to_buy):

		## Sample Blocks ##
		self.sma_period = period
		self.percent_difference_to_buy = percent_difference_to_buy
		# self.percent_difference_to_sell = percent_difference_to_sell

		## Ideas ##
		# - volatility of stock below certain threshold
		# - limit scope on sector / industry
		# - all other economic data can be used (P/E,R/E,...)
		# - covariance of sectors, industries --> aim for diversity in stocks
		# - covariance of stocks to each other --> avoid holding on to similar covariances in portfolio
		# - different parameter with averages
		#############

	def __run__(self):
		be = self.BacktestingEnvironment('2010-01-01','2011-01-01',1000000)
		be.run_period_with_algorithm()
		be.print_information()



## Script ##
if __name__ == '__main__':
	print('hello')
	sa = SampleAlgorithm(15,0.1) ## 15 day SMA for 0.1 percent difference to buy
	sa.__run__()






