## Calculator for Backtesting ## 

class Calculator:
	def __init__(self):
		pass

	@classmethod
	def average(self,arr,key):
		sum = 0
		for num in arr:
			sum += num[key]
		average = round(float(sum / len(arr)),2)
		return average

	@classmethod
	def variance(self,arr,key):
		c = Calculator()
		mean = c.average(arr,key)
		squared_differences = []
		for item in arr:
			squared_difference = (item[key] - mean)**2
			squared_differences.append({ key : squared_difference })
		variance = c.average(squared_differences,key)
		return variance

	@classmethod
	def covariance(self,arr1,arr2,key): ## arrays must be same length
		c = Calculator()
		mean1 = c.average(arr1,key)
		mean2 = c.average(arr2,key)
		tmp_points = []
		for index in range(0,len(arr1)):
			point = (arr1[index][key] - mean1)*(arr2[index][key] - mean2)
			tmp_points.append({ key : point })
		covariance = c.average(tmp_points,key)
		return covariance

	@classmethod
	def stdev(self,arr,key):
		c = Calculator()
		mean = c.average(arr,key)
		deviation = []
		for index in range(0,len(arr)):
			point = (arr[index][key] - mean)**2
			deviation.append({ key : point })
		av_deviation = c.average(deviation,key)
		st_dev = av_deviation**(0.5)
		return st_dev

	@classmethod
	def find_indexes(self,data,date_of_investment,date_of_return):
		for index in range(0,len(data)):
			if data[index]['date'] == date_of_investment:
				d_invest = index
			if data[index]['date'] == date_of_return:
				d_return = index
		return (d_invest,d_return)

	@classmethod
	def percent_change(self,data,index,increment,key):
		value = round(((data[index+increment][key] - data[index][key]) / (data[index][key])),2)
		return value

	@classmethod
	def percent_change_array(self,obj_arr,key):
		c = Calculator()
		percent_changes = []
		for index in range(0,(len(obj_arr)-1)):
			pchange = c.percent_change(obj_arr,index,1,key)
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
		value_portfolio = 0
		for asset in self.portfolio:
			value_portfolio += (asset['price_purchased']*asset['quantity'])
		return value_portfolio

	def assess_current_value(self,stock_data,date):
		new_value_portfolio = 0
		for date_point in stock_data:
			if date_point['date'] == date: ## date handshake
				for stock in self.portfolio:
					for new_data in date_point['data']:
						if stock['symbol'] == new_data['symbol']: ## symbol handshake
							new_value_portfolio += (new_data['price']*stock['quantity'])
		return new_value_portfolio

	def assess_total_returns(self,stock_data,date):
		total_returns = 0
		new_value_portfolio = self.assess_current_value(stock_data,date)
		returns = round(float((new_value_portfolio - self.value) / self.value),3)
		return returns

	def assess_returns_per_asset(self,stock_data,date):
		portfolio_returns_per_asset = []
		for date_point in stock_data:
			if date_point['date'] == date: ## date handshake
				for asset in self.portfolio:
					for new_data in date_point['data']:
						if asset['symbol'] == new_data['symbol']: ## symbol handshake
							## independent of quantity
							asset_returns = round(float((new_data['price'] - asset['price_purchased']) / asset['price_purchased']),3)
							portfolio_returns_per_asset.append({
								'symbol' : asset['symbol'],
								'quantity' : asset['quantity'],
								'returns' : asset_returns
								})
		return portfolio_returns_per_asset


class ReturnsCalculator:

	def __init__(self,stock_data,market_data,risk_free_returns):
		self.stock_data = stock_data
		self.market_data = market_data

		## returns preserve format
		self.stock_data_returns = self.returns_per_date(self.stock_data)
		self.market_data_returns = self.returns_per_date(self.market_data)
		self.risk_free_returns = risk_free_returns[1:] ## first value must be thrown out

	def returns_per_date(self,data):
		date_returns = []
		index = 1
		while index < len(data):
			data_per_date = []
			for stock in data[index]['data']:
				for stock_previous in data[index-1]['data']:
					if stock['symbol'] == stock_previous['symbol']: ## handshake
						returns_from_previous_date = round(float((stock['price'] - stock_previous['price']) / stock_previous['price']),3)
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
		self.portfolio = portfolio
		self.stock_data = stock_data
		self.market_data = market_data
		
		## calculate portfolio value
		self.pc = PortfolioCalculator(self.portfolio)
		self.portfolio_value = self.pc.value

		## calculate returns
		self.rc = ReturnsCalculator(self.stock_data,self.market_data,risk_free_returns)
		self.stock_data_returns = self.rc.stock_data_returns
		self.market_data_returns = self.rc.market_data_returns
		self.risk_free_returns = self.rc.risk_free_returns


	def alpha(self,beta):
		alpha = self.portfolio_returns - (self.risk_free + beta*(return_market - return_risk_free))
		return alpha
	
	def beta(self):
		for asset in self.portfolio_returns_arr:
			beta = round(float(self.c.covariance(self.portfolio_returns_arr,self.market_returns_arr,'returns') / self.c.variance(self.market_returns_arr,'returns')),3)
		return beta

	def sharpe(self):
		portfolio_stdev = self.c.stdev(self.portfolio_returns_arr,'returns')
		sharpe = round(float((self.portfolio_returns - self.risk_free) / portfolio_stdev),3)
		return sharpe

	def volatility(self):
		portfolio_stdev = self.c.stdev(self.portfolio_returns_arr,'returns')
		return portfolio_stdev

