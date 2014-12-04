from calculator import * 

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


class Portfolio_Test:
	def __init__(self):
		self.portfolio = [
			{'symbol' : 'IBM', 'quantity' : 20, 'price_purchased' : 200.00},
			{'symbol' : 'AAPL', 'quantity' : 10, 'price_purchased' : 300.00},
			{'symbol' : 'GOOG', 'quantity' : 200, 'price_purchased' : 500.00},
			{'symbol' : 'NFLX', 'quantity' : 50, 'price_purchased' : 400.00}
		]
		self.pc = PortfolioCalculator(self.portfolio)

	def test_value(self):
		assert self.pc.value == 127000

	def test_assess_current_value(self,stock_data,date):
		assert self.pc.assess_current_value(stock_data,date) == 144700

	def test_assess_total_returns(self,stock_data,date):
		assert self.pc.assess_total_returns(stock_data,date) == 0.13937

	def test_assess_returns_per_asset(self,stock_data,date):
		assert self.pc.assess_returns_per_asset(stock_data,date)[0]['symbol'] == 'IBM'
		assert self.pc.assess_returns_per_asset(stock_data,date)[0]['returns'] == 1.25
		
	def test_assess_returns_per_asset_per_date(self,stock_data):	
		assert self.pc.assess_returns_per_asset_per_date(stock_data)[0]['date'] == '2000/04/01'
		assert self.pc.assess_returns_per_asset_per_date(stock_data)[0]['total_returns'] == 0.18031
		assert self.pc.assess_returns_per_asset_per_date(stock_data)[0]['data'][0]['returns'] == 0.75

class Returns_Test:

	def __init__(self):
		## note format of portfolio is different than stock & market data (it has to be)
		## [{'symbol', 'data' : [{}]},]
		self.stock_data = [
				{'date': '2000/01/01', 'data': [ 
					{'symbol' : 'IBM', 'price' : 250.00},
					{'symbol' : 'AAPL', 'price' : 100.00},
					{'symbol' : 'GOOG', 'price' : 650.00},
					{'symbol' : 'NFLX', 'price' : 450.00},
				]},
				{'date': '2000/04/01', 'data' : [
					{'symbol' : 'IBM', 'price' : 350.00},
					{'symbol' : 'AAPL', 'price' : 90.00},
					{'symbol' : 'GOOG', 'price' : 600.00},
					{'symbol' : 'NFLX', 'price' : 440.00},
				]},
				{'date': '2000/07/01', 'data' : [
					{'symbol' : 'IBM', 'price' : 450.00},
					{'symbol' : 'AAPL', 'price' : 70.00},
					{'symbol' : 'GOOG', 'price' : 550.00},
					{'symbol' : 'NFLX', 'price' : 500.00},
				]},
				{'date': '2000/10/01', 'data': [
					{'symbol' : 'IBM', 'price' : 455.00},
					{'symbol' : 'AAPL', 'price' : 50.00},
					{'symbol' : 'GOOG', 'price' : 600.00},
					{'symbol' : 'NFLX', 'price' : 300.00},
				]}
			]

		self.market_data = [
				{'date': '2000/01/01', 'data': [
					{'symbol' : 'SP500', 'price' : 550.00}
				]},
				{'date': '2000/04/01', 'data': [
					{'symbol' : 'SP500', 'price' : 600.00}
				]},
				{'date': '2000/07/01', 'data': [
					{'symbol' : 'SP500', 'price' : 630.00}
				]},
				{'date': '2000/10/01', 'data': [
					{'symbol' : 'SP500', 'price' : 635.00}
				]},
		]

		self.risk_free_returns = [ ## based on historical yields==returns
				{'date': '2000/01/01', 'data': [
					{'symbol': 'risk_free', 'returns' : 0.030}
				]},
				{'date': '2000/04/01', 'data': [
					{'symbol': 'risk_free', 'returns' : 0.032}
				]},
				{'date': '2000/07/01', 'data': [
					{'symbol': 'risk_free', 'returns' : 0.031}
				]},
				{'date': '2000/10/01', 'data': [
					{'symbol': 'risk_free', 'returns' : 0.033}
				]}
		]

		self.returns_calc = ReturnsCalculator(self.stock_data,self.market_data,self.risk_free_returns)

	def test_format(self):
		assert type(self.returns_calc.stock_data_returns) == type([])
		assert type(self.returns_calc.stock_data_returns[0]) == type({})
		assert type(self.returns_calc.stock_data_returns[0]['data']) == type([])
		assert type(self.returns_calc.stock_data_returns[0]['data'][0]) == type({})
		assert type(self.returns_calc.stock_data_returns[0]['data'][0]['returns']) == type(1.0)

	def test_stocks(self):
		assert self.returns_calc.stock_data_returns[0]['data'][0]['returns'] ==  0.400
		assert self.returns_calc.stock_data_returns[0]['data'][1]['returns'] == -0.100
		assert self.returns_calc.stock_data_returns[0]['data'][2]['returns'] == -0.07692
		assert self.returns_calc.stock_data_returns[0]['data'][3]['returns'] == -0.02222

	def test_market(self):
		assert self.returns_calc.market_data_returns[0]['data'][0]['returns'] ==  0.09091

	def test_risk_free(self):
		assert self.returns_calc.risk_free_returns[0]['data'][0]['returns'] == 0.032



class Risk_Test:

	def __init__(self,portfolio,stock_data,market_data,risk_free_returns):
		self.rc = RiskCalculator(portfolio,stock_data,market_data,risk_free_returns)

	def test_alpha(self):
		assert self.rc.alpha() == 0.11800

	def test_betas(self):
		assert self.rc.beta() == 0.49565

	def test_sharpe(self):
		assert self.rc.sharpe() == 5.41614

	def test_volatility(self):
		assert self.rc.volatility() == 0.01949



## Run Calculator Tests ##

c = Calc_Test()
c.test_mean()
c.test_variance()
c.test_covariance()
c.test_stdev()
c.test_find_index()
c.test_percent_change()
c.test_percent_change_array()

## Run Portfolio Tests ##

pc = Portfolio_Test()
pc.test_value()
pc.test_assess_current_value(stock_data=Returns_Test().stock_data,date='2000/07/01')
pc.test_assess_total_returns(stock_data=Returns_Test().stock_data,date='2000/07/01')
pc.test_assess_returns_per_asset(stock_data=Returns_Test().stock_data,date='2000/07/01')
pc.test_assess_returns_per_asset_per_date(stock_data=Returns_Test().stock_data)

## Run Returns Tests ##

rt = Returns_Test()
rt.test_format()
rt.test_stocks()
rt.test_market()
rt.test_risk_free()

## Run Risk Tests ##

rm = Risk_Test(pc.portfolio,rt.stock_data,rt.market_data,rt.risk_free_returns)
rm.test_betas()
rm.test_sharpe()
rm.test_volatility()
rm.test_alpha()











