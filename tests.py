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
		self.calculator = Calculator()

	def test_mean(self):
		assert self.calculator.average(self.test_set1,'value') == 40

	def test_variance(self):
		assert self.calculator.variance(self.test_set1,'value') == 400

	def test_covariance(self):
		assert self.calculator.covariance(self.test_set1,self.test_set2,'value') == 40



## Run Tests ##

c = Calc_Test()
c.test_mean()
c.test_variance()
c.test_covariance()