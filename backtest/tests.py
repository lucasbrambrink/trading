from django.test import TestCase

from backtest.algorithm import BaseAlgorithm
from backtest.backtest import BacktestingEnvironment


class BasktestTest(TestCase):

    def setUp(self):
        self.algorithm_json = {
        'backtest': {
            'start_date': "2013-01-01",
            'end_date': "2014-01-01",
            'initial_balance': 1000000,
            'frequency': 12,
            'num_holdings': 1,
            },
        'algorithm': {
            'name' : 'Test',
            'sma': {
                'period1': 15,
                'period2': 10,
                'percent_difference_to_buy': 0.1,
                'appetite': 5
                },
            }
        }
        self.base = BaseAlgorithm(self.algorithm_json['algorithm'])
        self.backtest = BacktestingEnvironment(self.algorithm_json['backtest'], self.base.__dict__)

    def test_run_period_with_algorithm(self):
        self.assertTrue(self.backtest.run_period_with_algorithm(), "It should return true")