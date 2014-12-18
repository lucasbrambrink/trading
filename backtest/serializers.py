from rest_framework import serializers
from backtest.models import Stocks, Assets


class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = ('name', 'sector', 'industry', 'symbol')

class AssetsSerializer(serializers.ModelSerializer):
    stock = StocksSerializer()

    class Meta:
        model = Assets
        fields = ('stock', 'quantity', 'price_purchased', 'date')