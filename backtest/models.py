from django.db import models
from django.contrib.auth.models import User

from backtest.managers import StockManager


class Stocks(models.Model):
    objects = StockManager()

    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    symbol = models.CharField(max_length=6, unique=True, db_index=True)

    def natural_key(self):
        return self.symbol

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
        unique_together = (('stock', 'date'), )


class Algorithms(models.Model):
    user = models.ForeignKey(User)
    uuid = models.CharField(max_length=32, null=False, db_index=True)
    name = models.CharField(max_length=30)
    up_votes = models.IntegerField(default=0)
    json_string = models.CharField(max_length=500,default='None')

    class Meta:
        app_label = 'backtest'


class Backtests(models.Model):
    algorithm = models.ForeignKey(Algorithms)
    uuid = models.CharField(max_length=32, null=False, db_index=True)
    start_date = models.DateField()
    end_date = models.DateField()
    initial_balance = models.FloatField()
    frequency = models.IntegerField()
    num_holdings = models.IntegerField()

    class Meta:
        app_label = 'backtest'


class Assets(models.Model):
    backtest = models.ForeignKey(Backtests)
    stock = models.ForeignKey(Stocks)
    quantity = models.IntegerField()
    price_purchased = models.FloatField()
    date = models.DateField()

    class Meta:
        app_label = 'backtest'


class TreasuryBill(models.Model):
    date = models.DateField()
    three_month = models.FloatField()
    six_month = models.FloatField()
    one_year = models.FloatField()
    five_year = models.FloatField()
    ten_year = models.FloatField()
    thirty_year = models.FloatField()

    class Meta:
        app_label = 'backtest'


class Ratios(models.Model):
    stock = models.ForeignKey(Stocks)
    date = models.DateField()
    cash_revenue = models.FloatField(null=True)
    ev_ebitda = models.FloatField(null=True)
    market_cap = models.FloatField(null=True)
    pe_current = models.FloatField(null=True)
    return_equity = models.FloatField(null=True)

    class Meta:
        app_label = 'backtest'

