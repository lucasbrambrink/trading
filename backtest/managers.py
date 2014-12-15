from django.db import models


class StockManager(models.Manager):
    def get_by_natural_key(self, symbol):
        return self.get(symbol=symbol)