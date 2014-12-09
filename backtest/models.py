from django.db import models


class Stocks(models.Model):
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    symbol = models.CharField(max_length=6, unique=True, db_index=True)

    class Meta:
        app_label = 'backtest'


class Prices(models.Model):
    stock = models.ForeignKey(Stocks)
    date = models.DateField()
    open = models.CharField(max_length=20)
    high = models.CharField(max_length=20)
    low = models.CharField(max_length=20)
    close = models.CharField(max_length=20)

    class Meta:
        app_label = 'backtest'

"""
class Algorithms(models.Model):
    created_by = models.ForeignKey(Users)
    up_votes = models.IntegerField()


class Portfolios(models.Model):
    name = models.CharField(max_length=30)
    algorithm = models.ForeignKey(Algorithms)
    blocks = models.CharField(max_length=50) ## once we know what these are
    balance = models.CharField(max_length=25)


class Assets(models.Model):
    portfolio = models.ForeignKey(Portfolios)
    stock = models.ForeignKey(Stocks)
    quantity = models.IntegerField()
    price_purchased = models.CharField(max_length=10)
"""