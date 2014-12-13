from __future__ import absolute_import

from celery import shared_task

from .algorithm import BaseAlgorithm
from .backtest import BacktestingEnvironment
from .queues import ReturnsQueue


@shared_task
def run_backtest(algorithm_json):
    ## TODO: remove on production
    algorithm_json = {
        'backtest': {
            'id': '100',
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

    base = BaseAlgorithm(algorithm_json['algorithm'])
    backtest = BacktestingEnvironment(algorithm_json['backtest'], base.__dict__)

    returns_queue = ReturnsQueue(backtest.id)
    backtest.set_queue(returns_queue)

    backtest.run()