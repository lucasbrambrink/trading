from django.db import models


# Create your models here.

class Users(models.Model):
	email = models.EmailField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	# friends = models.ForeignKey(Users)
	avatar = models.CharField(max_length=10) ## if we have time

class Algorithms(models.Model):
	created_by = models.ForeignKey(Users)
	up_votes = models.IntegerField()

class Portfolios(models.Model):
	## User Key
	name = models.CharField(max_length=30)
	algorithm = models.ForeignKey(Algorithms)
	blocks = models.CharField(max_length=50) ## once we know what these are
	balance = models.CharField(max_length=25)

class Stocks(models.Model):
	name = models.CharField(max_length=100)
	sector = models.CharField(max_length=100)
	industry = models.CharField(max_length=100)
	symbol = models.CharField(max_length=6)

class Assets(models.Model):
	portfolio = models.ForeignKey(Portfolios)
	stock = models.ForeignKey(Stocks)
	quantity = models.IntegerField()
	price_purchased = models.CharField(max_length=10)

class Prices(models.Model):
	stock = models.ForeignKey(Stocks)
	date = models.CharField(max_length=15) ## dates are processed as strings
	open = models.CharField(max_length=20)
	high = models.CharField(max_length=20)
	low = models.CharField(max_length=20)
	close = models.CharField(max_length=20)

