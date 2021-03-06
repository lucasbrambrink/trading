from __future__ import absolute_import

from time import mktime
import json

from celery import shared_task

from backtest.algorithm import BaseAlgorithm
from backtest.backtest import BacktestingEnvironment
from backtest.queues import ReturnsQueue
from backtest.models import Algorithms


@shared_task
def run_backtest(algo_id, backtest_environ):
    algorithm = Algorithms.objects.get(uuid=algo_id)
    algorithm_json = {
        'algorithm': json.loads(algorithm.json_string)
    }
    base = BaseAlgorithm(algorithm_json['algorithm'])
    backtest = BacktestingEnvironment(backtest_environ, base.__dict__)
    returns_queue = ReturnsQueue(backtest.uuid)
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
    returns_queue = ReturnsQueue(backtest.uuid)

    for index, date in enumerate(backtest.dates_in_range):
        if index % math.floor(252/backtest.frequency) == 0:
            returns = random()
            returns_queue.enqueue(
                {
                    'returns': returns,
                    'date': 1000 * mktime(date.timetuple())
                }
            )
