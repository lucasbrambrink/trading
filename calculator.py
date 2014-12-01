## Calculator for Backtesting ## 

class Calculator:
	def __init__(self):
		pass

	@classmethod
	def average(self,arr):
		sum = 0
		for num in arr:
			sum += num
		average = round(float(sum / len(arr)),2)
		return average

	@classmethod
	def variance(self,arr):
		c = Calculator()
		mean_arr = c.average(arr)
		squared_differences = []
		for item in arr:
			squared_difference = (item - mean)**2
			squared_differences.append(squared_difference)
		variance = c.average(squared_differences)
		return variance

	@classmethod
	def covariance(self,arr1,arr2):
		c = Calculator()
		mean1 = c.average(arr1)
		mean2 = c.average(arr2)
		tmp_points = []
		for index in range(0,len(arr1)):
			point = (arr1[index] - mean1)*(arr2[index] - mean2)
			tmp_points.append(point)
		covariance = c.average(tmp_points)
		return covariance

	@classmethod
	def stdev(self,arr1):
		c = Calculator()
		mean = c.average(arr1)
		deviation = []
		for index in range(0,len(arr1)):
			point = (arr[index] - mean)**2
			deviation.append(point)
		av_deviation = c.average(deviation)
		st_dev = av_deviation**(0.5)
		return st_dev

	@classmethod
	def alpha(self,**kwargs):
		c = Calculator()
		pass

	@classmethod	
	def beta(self,stock,benchmark):
		c = Calculator()
		pc_stock = c.percent_change_array(stock)
		pc_benchmark = c.percent_change_array(benchmark)
		beta = round(float(c.covariance(pc_stock,pc_benchmark) / c.variance(pc_benchmark)),3)
		return beta

	@classmethod	
	def sharpe(self,**kwargs):
		pass

	@classmethod
	def total_returns(self,*args):
		pass

	@classmethod
	def volatility(self,**kwargs):
		pass

	@classmethod
	def find_indexes(self,data,date_of_investment,date_of_return,key='close'):
		for index in range(0,len(data)):
			if data[index]['date'] == date_of_investment:
				d_invest = index
			if data[index]['date'] == date_of_return:
				d_return = index
		return (d_invest,d_return)

	@classmethod
	def percent_change(self,data,index,increment,key):
		value = round(((data[index+increment][key] - data[index][key]) / (parsed_data[index][key])),2)
		return value

	@classmethod
	def percent_change_array(self,obj_arr):
		c = Calculator()
		percent_changes = []
		for index in range(0,(len(arr)-1)):
			pchange = c.percent_change(obj_arr,index,1,'close')
			percent_changes.append({
				'date' : obj_arr[index]['date'],
				'pchange' : pchange
				})
		return percent_changes


