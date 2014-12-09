class Test:
	def __init__(self,**kwargs):
		self.one = 'default'
		self.two = 'default'
		self.three = 'default'
		for key in kwargs:
			setattr(self,key,kwargs[key])

		print(self.one,self.two,self.three)



test = {'one':1,'two':2}
print(Test(**test))