import re
def a():
	a = ['12345','1234','12345678']
	if len([re.search('123',c) for c in a]) != 0:
		return(True)
	return False
print(a())