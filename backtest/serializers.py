from rest_framework import serializers
from backtest.models import (Stocks, Assets, RiskMetrics)


class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = ('name', 'sector', 'industry', 'symbol')


class AssetsSerializer(serializers.ModelSerializer):
    stock = StocksSerializer()

    class Meta:
        model = Assets
        fields = ('stock', 'quantity', 'price_purchased', 'date')


class RiskMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskMetrics
        fields = ('date', 'alpha', 'beta' ,'sharpe', 'volatility', 'returns')