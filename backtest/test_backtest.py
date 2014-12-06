from backtest import *
import csv

class CollectData:

	def __init__(self,csv_target):
		self.csv_file = csv_target
		self.all_dates = self.prepare_dates_for_data_collection()

	def prepare_dates_for_data_collection(self):
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

	def market_snapshot_by_date(self,date):
		## price == closing price
		snapshot = []
		with open(self.csv_file,'r') as stock_data:
			data = csv.reader(stock_data)
			for row in data:
				if str(row[1]) == date:
					snapshot.append({
						'symbol' : row[0],
						'price' : float(row[5])
						})
		day = { 'date' : date, 'data' : snapshot}
		return day

	def market_snapshot_by_stock(self,symbol):
		## price == closing price
		with open(self.csv_file, 'r') as stock_data:
			market_data = []	
			data = csv.reader(stock_data)
			for row in data:
				try:
					if str(row[0]) == symbol:
						market_data.append({
							'date' : row[0],
							'price' : float(row[5])
							})
				except:
					continue
			stock = { 'symbol' : symbol, 'data' : market_data}
			return stock

	def collect_stock_symbols(self):
		symbols = []
		with open(self.csv_file, 'r') as stock_data:
			data = csv.reader(stock_data)
			for row in data:
				if row[0] not in symbols:
					symbols.append(row[0])
				if len(symbols) > 11:
					break
		return symbols

	def split_date_into_ints(self,date):
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





class SampleAlgorithm:
## marks stocks whose 30 day SMA (simple moving average) has changed by more than 10%

	def __init__(self):
		self.initial_balance = 1000000
		self.start_date = '2010-01-01'
		self.end_date = '2011-01-01' ## let's just try one year for now

		## data class ##
		self.cd = CollectData('csv_files/stock_prices.csv')
		
		## relevant dates ##
		self.dates_in_range = self.collect_dates_in_range()
		
		## data ##
		# self.relevant_data = self.fetch_data_in_range()
		self.stocks_in_market = self.cd.collect_stock_symbols()

		
		## calculator ##
		self.c = Calculator()

		## averages
		self.averages = self.get_simple_moving_averages()

		## stocks to buy!!
		self.stocks_to_buy = self.test_averages()

	def collect_dates_in_range(self):
		dates_in_range = []
		start_year,start_month,start_day = self.cd.split_date_into_ints(self.start_date)
		end_year,end_month,end_day = self.cd.split_date_into_ints(self.end_date)
		for date in self.cd.prepare_dates_for_data_collection():
			year,month,day = self.cd.split_date_into_ints(date)
			if start_year <= year <= end_year:
				if start_month <= month <= end_month:
					dates_in_range.append(date)
		return dates_in_range

	def fetch_data_in_range(self):
		relevant_data = []
		for date in self.dates_in_range:
			days_stock_data = self.cd.market_snapshot_by_date(date)
			relevant_data.append(days_stock_data)
		return relevant_data

	def get_simple_moving_averages(self):
		averages = []
		for symbol in self.stocks_in_market:
			prices = []
			this_symbol_data = self.cd.market_snapshot_by_stock(symbol)
			for data in this_symbol_data['data']:
				for date in self.dates_in_range:
					if date == data['date']: ## date handshake
						if len(prices) < 30: ## let's do a 30 day SMA
							print(data['price'])
							prices.append({'price' : data['price']})
						else:
							sma = self.c.average(prices,'price')
							print(sma)
							averages.append({
								'symbol' : symbol,
								'sma' : sma
								})
							prices = []
		return averages

	def test_averages(self):
		stocks_to_buy = []
		for average in self.averages:
			if average['sma'] > 0.1:
				stocks_to_buy.append(average)
		return stocks_to_buy



print(SampleAlgorithm().test_averages())






