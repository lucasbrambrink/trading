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
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()

    class Meta:
        app_label = 'backtest'

class Algorithms(models.Model):
    # user = models.ForeignKey(Users)
    name = models.CharField(max_length=30)
    # created_by = models.ForeignKey(Users)
    # up_votes = models.IntegerField()

    class Meta:
        app_label = 'backtest'


class Assets(models.Model):
    algorithm = models.ForeignKey(Algorithms)
    stock = models.ForeignKey(Stocks)
    quantity = models.IntegerField()
    price_purchased = models.CharField(max_length=10)
    date = models.DateField()

    class Meta:
        app_label = 'backtest'
