## Calculator for Backtesting ## 

class Calculator:

	@staticmethod
	def average(arr,key):
		"""
		:param arr1: [{ 'key' : value },...]
		:param key: key

		:return: float
		"""
		sum = 0
		for num in arr:	
			sum += num[key]
		average = round(float(sum / len(arr)),5)
		return average

	@staticmethod
	def variance(arr,key):
		"""
		:param arr1: [{ 'key' : value },...]
		:param key: key

		:return: float
		"""
		mean = Calculator.average(arr,key)
		squared_differences = []
		for item in arr:
			squared_difference = (item[key] - mean)**2
			squared_differences.append({ key : squared_difference })
		variance = Calculator.average(squared_differences,key)
		return variance

	@staticmethod
	def covariance(arr1,arr2,key): ## arrays must be same length
		"""
		:param arr1: [{ 'key' : value },...]
		:param arr2: [{ 'key' : value },...]
		:param key: key

		:return: float
		"""
		if len(arr1) > len(arr2):
			arr1 = arr1[:len(arr2)]
		if len(arr1) < len(arr2):
			arr2 = arr2[:len(arr1)] ## shorten the arrays to complementary lengths
		## by throwing out last elements -- or throw error, depending on what we want
		mean1 = Calculator.average(arr1,key)
		mean2 = Calculator.average(arr2,key)
		tmp_points = []
		for index in range(0,len(arr1)):
			point = (arr1[index][key] - mean1)*(arr2[index][key] - mean2)
			tmp_points.append({ key : point })
		covariance = Calculator.average(tmp_points,key)
		return covariance

	@staticmethod
	def stdev(arr,key):
		"""
		:param arr1: [{ 'key' : value },...]
		:param key: key

		:return: float
		"""
		mean = Calculator.average(arr,key)
		deviation = []
		for index in range(0,len(arr)):
			point = (arr[index][key] - mean)**2
			deviation.append({ key : point })
		av_deviation = Calculator.average(deviation,key)
		st_dev = av_deviation**(0.5)
		return st_dev

	@staticmethod
	def find_indexes(data,date_of_investment,date_of_return):
		"""
		:param data: [{ 'date' : 'yyyy/mm/dd',...},...]
		:param date_of_investment: "yyyy/mm/dd"
		:param date_of_return: "yyyy/mm/dd"

		:return: tuple(index_investment,index_return)
		"""
		for index in range(0,len(data)):
			if data[index]['date'] == date_of_investment:
				d_invest = index
			if data[index]['date'] == date_of_return:
				d_return = index
		return (d_invest,d_return)

	@staticmethod
	def percent_change_simple(point1,point2):
		"""
		:param1: integer
		:param2: integer
		:return: float
		"""
		value = round(((point2 - point1) / point1),5)
		return value

	@staticmethod
	def percent_change(data,index,increment,key):
		"""
		:param data: [{ 'key' : value,},...]
		:param index: integer
		:param increment: integer
		:param key: key

		:return: float
		"""
		value = round(((data[index+increment][key] - data[index][key]) / (data[index][key])),5)
		return value

	@staticmethod
	def percent_change_array(obj_arr,key):
		"""
		:param obj_arr: [{ 'key' : value,},...]
		:param key: key

		:return: [{ 'date' : date, 'returns' : value},...]
		"""
		percent_changes = []
		for index in range(0,(len(obj_arr)-1)):
			pchange = Calculator.percent_change(obj_arr,index,1,key)
			percent_changes.append({
				'date' : obj_arr[index]['date'],
				'returns' : pchange
				})
		return percent_changes


class PortfolioCalculator:

	def __init__(self,portfolio):
		self.portfolio = portfolio
		self.value = self.value()

	def value(self):
		"""
		:return: float
		"""
		value_portfolio = 0
		for asset in self.portfolio:
			value_portfolio += (asset['price_purchased']*asset['quantity'])
		return value_portfolio

	def assess_current_value(self,stock_data,date):
		"""
		:param stock_data: [{ 'date' : date, 'data' : [{},...]},...]
		:param date: 'yyyy/mm/dd'

		:return: float
		"""
		new_value_portfolio = 0
		for date_point in stock_data:
			if date_point['date'] == date: ## date handshake
				for stock in self.portfolio:
					for new_data in date_point['data']:
						if stock['symbol'] == new_data['symbol']: ## symbol handshake
							new_value_portfolio += (new_data['price']*stock['quantity'])
		return new_value_portfolio

	def assess_total_returns(self,stock_data,date):
		"""
		:param stock_data: [{ 'date' : date, 'data' : [{},...]},...]
		:param date: 'yyyy/mm/dd'

		:return: float
		"""
		total_returns = 0
		new_value_portfolio = self.assess_current_value(stock_data,date)
		returns = round(float((new_value_portfolio - self.value) / self.value),5)
		return returns

	def assess_returns_per_asset(self,stock_data,date):
		"""
		:param stock_data: [{ 'date' : date, 'data' : [{},...]},...]
		:param date: 'yyyy/mm/dd'

		:return: [{'symbol','quantity','returns'},...]
		"""
		portfolio_returns_per_asset = []
		for date_point in stock_data:
			if date_point['date'] == date: ## date handshake
				for asset in self.portfolio:
					for new_data in date_point['data']:
						if asset['symbol'] == new_data['symbol']: ## symbol handshake
							## independent of quantity
							asset_returns = round(float((new_data['price'] - asset['price_purchased']) / asset['price_purchased']),5)
							portfolio_returns_per_asset.append({
								'symbol' : asset['symbol'],
								'quantity' : asset['quantity'],
								'returns' : asset_returns
								})
		return portfolio_returns_per_asset

	def assess_returns_per_asset_per_date(self,stock_data):
		"""
		:param stock_data: [{ 'date' : date, 'data' : [{},...]},...]

		:return: [{'date','data': [{},...]},...]
		"""
		portfolio_returns_per_asset_per_date = []
		for index,date_point in enumerate(stock_data):
			if index == 0:
				continue
			portfolio_returns_per_asset_per_date.append({
				'date' : date_point['date'],
				'total_returns' : self.assess_total_returns(stock_data,date_point['date']),
				'data' : self.assess_returns_per_asset(stock_data,date_point['date'])
				})
		return portfolio_returns_per_asset_per_date


class ReturnsCalculator:

	def __init__(self,stock_data,market_data,risk_free_returns):
		"""
		:param stock_data: [{ 'date' : date, 'data' : [{},...]},...]
		:param market_data: [{ 'date' : date, 'data' : [{}]},...]
		:param risk_free_returns: [{ 'date' : date, 'data' : [{}]},...]
		"""

		self.stock_data = stock_data
		self.market_data = market_data

		## returns preserve format
		self.stock_data_returns = self.returns_per_date(self.stock_data)
		self.market_data_returns = self.returns_per_date(self.market_data)
		self.risk_free_returns = risk_free_returns[1:] ## first value must be thrown out

	def returns_per_date(self,data):
		"""
		:param data: [{ 'date' : date, 'data' : [{},...]},...]

		:return: [{'date','data': [{'symbol','returns'},...]},...]
		"""
		date_returns = []
		index = 1
		while index < len(data):
			data_per_date = []
			for stock in data[index]['data']:
				for stock_previous in data[index-1]['data']:
					if stock['symbol'] == stock_previous['symbol']: ## handshake
						returns_from_previous_date = round(float((stock['price'] - stock_previous['price']) / stock_previous['price']),5)
				data_per_date.append({ 
					'symbol' : stock['symbol'], 
					'returns' : returns_from_previous_date
					})
			date_returns.append({
				'date' : data[index]['date'],
				'data' : data_per_date
				})
			index += 1
		return date_returns


## This will serve as a superclass, in that it will execute all the calculations in __init__

class RiskCalculator:
	def __init__(self,portfolio,stock_data,market_data,risk_free_returns):
		"""
		:param portfolio: [{'symbol','quantity','price_purchased'}]
		:param stock_data: [{ 'date' : date, 'data' : [{},...]},]
		:param market_data: [{ 'date' : date, 'data' : [{},...]},]
		:param risk_free_returns: [{ 'date' : date, 'data' : [{}]},...]
		"""
		self.portfolio = portfolio
		self.stock_data = stock_data
		self.market_data = market_data
		
		## calculate portfolio value
		self.pc = PortfolioCalculator(self.portfolio)
		self.portfolio_value = self.pc.value

		## calculate market returns
		self.rc = ReturnsCalculator(self.stock_data,self.market_data,risk_free_returns)
		self.stock_data_returns = self.rc.stock_data_returns
		self.market_data_returns = self.rc.market_data_returns
		self.risk_free_returns = self.rc.risk_free_returns
		
		## calculate portfolio returns
		self.portfolio_returns = self.pc.assess_returns_per_asset_per_date(self.stock_data)
		
		## initialize Calculator
		self.c = Calculator()

		## establish complementary arrays of portfolio and market returns
		self.portfolio_returns_array,self.market_returns_array = self.complementary_arrays()


	def complementary_arrays(self):
		"""
		:returns: [float,...],[float,...]
		"""
		portfolio_returns_array = []
		market_returns_array = []
		for portfolio_date_point in self.portfolio_returns:
			for market_date_point in self.market_data_returns:
				if portfolio_date_point['date'] == market_date_point['date']: ## date handshake
					portfolio_returns_array.append({'returns' : portfolio_date_point['total_returns']})
					market_returns_array.append(market_date_point['data'][0])
		return portfolio_returns_array,market_returns_array

	def alpha(self):
		"""
		:returns: float
		"""
		beta = self.beta()
		alpha = self.portfolio_returns_array[-1]['returns'] - (self.risk_free_returns[-1]['data'][-1]['returns'] + beta*(self.market_returns_array[-1]['returns'] - self.risk_free_returns[-1]['data'][-1]['returns']))
		return round(alpha,5)
	
	def beta(self):
		"""
		:returns: float
		"""
		beta = round(float(self.c.covariance(self.portfolio_returns_array,self.market_returns_array,'returns') / self.c.variance(self.market_returns_array,'returns')),5)
		return beta

	def sharpe(self):
		"""
		:returns: float
		"""
		portfolio_stdev = self.c.stdev(self.portfolio_returns_array,'returns')
		sharpe = round(float((self.portfolio_returns_array[-1]['returns'] - self.risk_free_returns[-1]['data'][-1]['returns']) / portfolio_stdev),5)
		return sharpe

	def volatility(self):
		"""
		:returns: float
		"""
		portfolio_stdev = round(self.c.stdev(self.portfolio_returns_array,'returns'),5)
		return portfolio_stdev

