from calculator import Calculator 

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
			{'date': '2000/01/01', 'pchange': 1.0},
		    {'date': '2000/01/01', 'pchange': 1.0}]

## Run Tests ##

c = Calc_Test()
c.test_mean()
c.test_variance()
c.test_covariance()
c.test_stdev()
c.test_find_index()
c.test_percent_change()
c.test_percent_change_array()