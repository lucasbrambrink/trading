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

	@classmethod
	def total_returns(self,portfolio,current_prices):
		value_portfolio = 0
		current_value = 0
		for asset in portfolio:
			value_portfolio += (asset['price_purchased']*asset['quantity'])
			for price in current_prices:
				if price['symbol'] == asset['symbol']:
					current_value += (price['current_price']*asset['quantity'])
		returns = round(float((current_value - value_portfolio) / value_portfolio),3)
		return returns

	@classmethod
	def returns_array(self,portfolio,current_prices):
		returns = []
		for asset in portfolio:
			for price in current_prices:
				if price['symbol'] == asset['symbol']:
					returns_per_share = round(float((price['current_price'] - asset['price_purchased']) / asset['price_purchased']),3)
					returns.append({ 'symbol' : asset['symbol'], 'returns' : returns_per_share})
		return returns

class RiskCalculator:
	def __init__(self,portfolio,current_prices,risk_free,market_data):
		self.c = Calculator()
		self.portfolio = portfolio
		self.current_prices = current_prices
		self.risk_free = risk_free
		self.market_returns = self.c.percent_change(market_data,0,(len(market_data)-1),'price')
		self.market_returns_arr = self.c.percent_change_array(market_data,'price')
		self.portfolio_returns = self.c.total_returns(self.portfolio,self.current_prices)
		self.portfolio_returns_arr = self.c.returns_array(self.portfolio,self.current_prices)

	def alpha(self,beta):
		alpha = self.portfolio_returns - (self.risk_free + beta*(return_market - return_risk_free))
		return alpha
	
	def beta(self):
		beta = round(float(self.c.covariance(self.portfolio_returns_arr,self.market_returns_arr,'returns') / self.c.variance(self.market_returns_arr,'returns')),3)
		return beta

	def sharpe(self):
		portfolio_stdev = self.c.stdev(self.portfolio_returns_arr,'returns')
		sharpe = round(float((self.portfolio_returns - self.risk_free) / portfolio_stdev),3)
		return sharpe

	def volatility(self):
		portfolio_stdev = self.c.stdev(self.portfolio_returns_arr,'returns')
		return portfolio_stdev

