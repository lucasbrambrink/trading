from calculator import Calculator,RiskCalculator 

class Calc_Test:

	def __init__(self):
		self.test_set1 = [
			{ "date" : "2000/01/01", 'value' : 10},
			{ "date" : "2000/01/02", 'value' : 20},
			{ "date" : "2000/01/03", 'value' : 30},
			{ "date" : "2000/01/04", 'value' : 40},
			{ "date" : "2000/01/05", 'value' : 50},
			{ "date" : "2000/01/06", 'value' : 60},
			{ "date" : "2000/01/07", 'value' : 70},
		]
		self.test_set2 = [
			{ "date" : "2000/01/01", 'value' : 35},
			{ "date" : "2000/01/02", 'value' : 36},
			{ "date" : "2000/01/03", 'value' : 37},
			{ "date" : "2000/01/04", 'value' : 38},
			{ "date" : "2000/01/05", 'value' : 39},
			{ "date" : "2000/01/06", 'value' : 40},
			{ "date" : "2000/01/07", 'value' : 41},
		]
		self.test_set3 = [
			{ "date" : "2000/01/01", 'value' : 10},
			{ "date" : "2000/01/01", 'value' : 20},
			{ "date" : "2000/01/01", 'value' : 40},
		]
		self.calculator = Calculator()

	def test_mean(self):
		assert self.calculator.average(self.test_set1,'value') == 40

	def test_variance(self):
		assert self.calculator.variance(self.test_set1,'value') == 400

	def test_covariance(self):
		assert self.calculator.covariance(self.test_set1,self.test_set2,'value') == 40

	def test_stdev(self):
		assert self.calculator.stdev(self.test_set1,'value') == 20

	def test_find_index(self):
		assert self.calculator.find_indexes(self.test_set1,'2000/01/02','2000/01/06') == (1,5)

	def test_percent_change(self):
		assert self.calculator.percent_change(self.test_set1,0,1,'value') == 1

	def test_percent_change_array(self):
		assert self.calculator.percent_change_array(self.test_set3,'value') == [
			{'date': '2000/01/01', 'returns': 1.0},
		    {'date': '2000/01/01', 'returns': 1.0}]


class Risk_Test:
	def __init__(self):
		self.portfolio = [
			{'symbol' : 'IBM', 'quantity' : 20, 'price_purchased' : 200.00},
			{'symbol' : 'AAPL', 'quantity' : 10, 'price_purchased' : 300.00},
			{'symbol' : 'GOOG', 'quantity' : 200, 'price_purchased' : 500.00},
			{'symbol' : 'NFLX', 'quantity' : 50, 'price_purchased' : 400.00}
		]

		self.stock_data = [
			[
				{'date': '2000/01/01', 'symbol' : 'IBM', 'current_price' : 250.00},
				{'date': '2000/01/01', 'symbol' : 'AAPL', 'current_price' : 100.00},
				{'date': '2000/01/01', 'symbol' : 'GOOG', 'current_price' : 650.00},
				{'date': '2000/01/01', 'symbol' : 'NFLX', 'current_price' : 450.00},
			],[
				{'date': '2000/04/01', 'symbol' : 'IBM', 'current_price' : 350.00},
				{'date': '2000/04/01', 'symbol' : 'AAPL', 'current_price' : 90.00},
				{'date': '2000/04/01', 'symbol' : 'GOOG', 'current_price' : 600.00},
				{'date': '2000/04/01', 'symbol' : 'NFLX', 'current_price' : 440.00},
			],[
				{'date': '2000/07/01', 'symbol' : 'IBM', 'current_price' : 450.00},
				{'date': '2000/07/01', 'symbol' : 'AAPL', 'current_price' : 70.00},
				{'date': '2000/07/01', 'symbol' : 'GOOG', 'current_price' : 550.00},
				{'date': '2000/07/01', 'symbol' : 'NFLX', 'current_price' : 500.00},
			],[
				{'date': '2000/10/01', 'symbol' : 'IBM', 'current_price' : 455.00},
				{'date': '2000/10/01', 'symbol' : 'AAPL', 'current_price' : 50.00},
				{'date': '2000/10/01', 'symbol' : 'GOOG', 'current_price' : 600.00},
				{'date': '2000/10/01', 'symbol' : 'NFLX', 'current_price' : 300.00},
			]
		]

		self.risk_free_rate = 0.030 ##suppose this is 3 months later
		self.market_data = [
			{'date': '2000/01/01', 'symbol' : 'SP500', 'price' : 550.00},
			{'date': '2000/04/01', 'symbol' : 'SP500', 'price' : 600.00},
			{'date': '2000/07/01', 'symbol' : 'SP500', 'price' : 630.00},
			{'date': '2000/10/01', 'symbol' : 'SP500', 'price' : 635.00}
		]
		self.risk_calc = RiskCalculator(self.portfolio,self.current_values,self.risk_free_rate,self.market_data)

	def test_alpha(self):
		pass

	def test_beta(self):
		assert self.risk_calc.beta()
		pass

	def test_sharpe(self):
		pass

	def test_volatility(self):
		pass

	def test_total_returns(self):
		pass

	def test_returns_array(self):
		pass


## Run Tests ##

c = Calc_Test()
c.test_mean()
c.test_variance()
c.test_covariance()
c.test_stdev()
c.test_find_index()
c.test_percent_change()
c.test_percent_change_array()

## Run Risk Tests ##

rc = Risk_Test()
rc.test_beta()










