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


class PorfolioCalculator:

	def __init__(self,portfolio):
		self.portfolio = portfolio
		self.value = self.initial_value()

	def initial_value(self):
		value_portfolio = 0
		for asset in portfolio:
			value_portfolio += (asset['price_purchased']*asset['quantity'])
		return value_portfolio


class MarketCalculator:

	def __init__(self,stock_data,market_data,risk_free_returns):
		self.stock_data = stock_data
		self.market_data = market_data

		## returns preserve format
		self.stock_data_returns = self.returns_per_date(self.stock_data)
		self.market_data_returns = self.returns_per_date(self.market_data)
		self.risk_free_returns = risk_free_returns

	def returns_per_date(self,data):
		date_returns = []
		index = 1
		while index < len(data):
			data = []
			for stock in data[index]['data']:
				for stock_previous in data[index-1]['data']:
					if stock['symbol'] == stock_previous['symbol']: ## handshake
						returns_from_previous_date = round(float((stock['price'] - stock_previous['price']) / stock_previous['price']),3)
				data.append({ 
					'symbol' : stock['symbol'], 
					'returns' : returns_from_previous_date
					})
			date_returns.append({
				'date' : data[index]['date'],
				'data' : data
				})
		return date_returns

	
class AssessCurrentValue:

	def __init__(self):
		pass

	@classmethod
	def total_returns(self,portfolio,market_data,key):
		value_portfolio = 0
		current_value = 0
		total = []
		for date in portfolio:
			for asset in date:
				value_portfolio += (asset['price_purchased']*asset['quantity'])
				for price in current_prices:
					if price['symbol'] == asset['symbol']:
						current_value += (price['price']*asset['quantity'])
			returns = round(float((current_value - value_portfolio) / value_portfolio),3)
			total.append(returns)
		return sum(total)






class RiskCalculator:
	def __init__(self,portfolio,stock_data,risk_free,market_data):
		self.c = Calculator()
		self.portfolio = portfolio
		self.stock_data = stock_data
		self.risk_free = risk_free
		self.market_data = market_data

		## calculate the returns of the data

		self.market_total_returns = self.c.total_returns(market_data,0,(len(market_data)-1),'price')
		self.market_returns_arr = self.c.percent_change_array(market_data,'price')
		self.portfolio_total_returns = self.c.total_returns(self.portfolio,self.stock_data)
		self.portfolio_returns_arr = self.c.returns_array(self.portfolio,self.stock_data)

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

