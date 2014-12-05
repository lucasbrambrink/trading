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
				first_half, second_half = [],[]
				for date in range(1,32): ## it is okay for all months to go to 31 bc many of the dates wont be in the DB regardless (stock market closed)
					string = str(year) + "-" + str(month_format) + "-"
					if date < 10:
						string += "0" + str(date)
					else:
						string += str(date)
					if date < 16:
						first_half.append(string)
					else:
						second_half.append(string)
				one_year.append({
					'month' : month_format,
					'first_half' : first_half,
					'second_half' : second_half
					})
			all_dates.append({
				'year' : year,
				'data' : one_year
				})
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
		return snapshot




class SampleAlgorithm:

	def __init__(self):
		start_date = '2000-01-01'
		end_date = '2001-01-01' ## let's just try one year for now


print(CollectData('csv_files/stock_prices.csv').market_snapshot_by_date('2010-06-01'))

