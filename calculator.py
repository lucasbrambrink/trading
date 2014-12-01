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
	def covariance(self,arr1,arr2,key):
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
		mean = c.average(arr1)
		deviation = []
		for index in range(0,len(arr1)):
			point = (arr[index][key] - mean)**2
			deviation.append(point)
		av_deviation = c.average(deviation,key)
		st_dev = av_deviation**(0.5)
		return st_dev

	@classmethod
	def alpha(self,return_portfolio,return_market,return_risk_free,beta):
		alpha = return_portfolio - (return_risk_free + beta*(return_market - return_risk_free))
		return alpha

	@classmethod	
	def beta(self,stock,benchmark):
		c = Calculator()
		pc_stock = c.percent_change_array(stock)
		pc_benchmark = c.percent_change_array(benchmark)
		beta = round(float(c.covariance(pc_stock,pc_benchmark,'pchange') / c.variance(pc_benchmark,'pchange')),3)
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
	def find_indexes(self,data,date_of_investment,date_of_return):
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


