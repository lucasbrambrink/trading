## Backtesting Suite ## 

class Backtester:
	def __init__(self, **kwargs):
		# self.portfolio = portfolio ## accepts 'porfolio' kwarg as array
		self.portfolio_value = []
		pass

	def run_test(self,**kwargs):
		pass

	@classmethod
	def get_portfolio_value(**kwargs):
		pass

	@classmethod
	def establish_benchmark(self):
		data = csv.reader(open('algotrade/spindex.csv', newline=''))
		parsed_data = []
		index = 0
		for row in data:
			if 0 < index < 3750: ## Jan 1, 2000
				parsed_data.append({
						"date" : row[0], 
						"value": float(row[4])
					})
			index += 1
		a = len(parsed_data)-1
		b=0
		returns = []
		sum_returns = 0
		while a >= 0:
			value = round(((parsed_data[a]['value'] - parsed_data[-1]['value']) / (parsed_data[-1]['value'])),2)
			if value > 0:
				sum_returns += value
			adj_return = { 
				'date' : b, #parsed_data[a]['date'],
			    'value' : value
			    }
			returns.append(adj_return)
			a -= 1
			b += 1
		return returns

	@classmethod
	def calculate_risks(self,**kwargs):
		pass
		# c = Calculator()
		# risks = {
		# 	'alpha' = c.alpha(),
		# 	'beta' = c.beta(),
		# 	'sharpe' = c.sharpe(),
		# 	'returns' = c.total_returns(),
		# 	'volatility' = c.volatility()
		# 	}
		# return risks

	@classmethod
	def fetch_stock_data(self,symbol):
		data = csv.reader(open('stock_prices.csv',newline=''))
		stock_data = []
		for row in data:
			if row[0] == symbol:
				stock_data.append({
					'date' : row[1], 
					'open' : row[2], 
					'high' : row[3], 
					'low' : row[4],
					'close' : row[5]
					})
		return stock_data
