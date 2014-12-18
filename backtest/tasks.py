from __future__ import absolute_import

from time import mktime
import json

from celery import shared_task

from backtest.algorithm import BaseAlgorithm
from backtest.backtest import BacktestingEnvironment
from backtest.queues import ReturnsQueue
from backtest.models import Algorithms


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

@shared_task
def test_backtest(algo_id, backtest_environ):
    import math
    from random import random
    from .queues import ReturnsQueue

    print('Celery: start backtest!!!')

    algorithm = Algorithms.objects.get(uuid=algo_id)
    algorithm_json = {
        'algorithm': json.loads(algorithm.json_string)
    }
    base = BaseAlgorithm(algorithm_json['algorithm'])
    backtest = BacktestingEnvironment(backtest_environ, base.__dict__)
    print(backtest.start_date, backtest.end_date, backtest.dates_in_range)
    returns_queue = ReturnsQueue(backtest.uuid)

    for index, date in enumerate(backtest.dates_in_range):
        if index % math.floor(252/backtest.frequency) == 0:
            returns = random()
            print(date, returns)
            returns_queue.enqueue(
                {
                    'returns': returns,
                    'date': 1000 * mktime(date.timetuple())
                }
            )
