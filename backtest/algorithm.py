
## Algorithms built from Blocks ##
from backtest.blocks import *
from backtest.models import Algorithms
import re
import json

class BaseAlgorithm:

    def __init__(self,algorithm):
        self.blocks_buy = []
        self.blocks_sell = []
        self.conditions_buy = []
        self.conditions_sell = []
        self.user_id = algorithm['user_id']
        self.name = algorithm['name']
        self.uuid = algorithm['uuid']
        self.json_string = json.dumps(algorithm)
        self.id = Algorithms.objects.get(uuid=self.uuid).id
        for key in algorithm['block']:
            ## active conditions ##
            if key == 'sma':
                for sma in algorithm['block'][key]['buy']:
                    self.blocks_buy.append(SMA_Block(**sma))
                for sma in algorithm['block'][key]['sell']:
                    self.blocks_sell.append(SMA_Block(**sma))
            if key == 'volatility':
                for volatility in algorithm['block'][key]['buy']:
                    self.blocks_buy.append(Volatility_Block(**volatility))
                for volatility in algorithm['block'][key]['sell']:
                    self.blocks_sell.append(Volatility_Block(**volatility))
            if key == 'covariance': 
                for covariance in algorithm['block'][key]['buy']:
                    self.blocks_buy.append(Covariance_Block(**covariance))
                for covariance in algorithm['block'][key]['sell']:
                    self.blocks_sell.append(Covariance_Block(**covariance))
            if key == 'event':
                for event in algorithm['block'][key]['buy']:
                    self.blocks_buy.append(Event_Block(**event))
                for event in algorithm['block'][key]['sell']:
                    self.blocks_sell.append(Event_Block(**event))
            if key == 'ratio':
                for ratio in algorithm['block'][key]['buy']:
                    self.blocks_buy.append(Ratio_Block(**ratio))
                for ratio in algorithm['block'][key]['sell']:
                    self.blocks_sell.append(Ratio_Block(**ratio))
            ## passive conditions ##
            if key == 'thresholds' or key == 'diversity' or key == 'crisis':
                for condition in algorithm['block'][key]['buy']:
                    self.conditions_buy.append({key: condition})
                for condition in algorithm['block'][key]['sell']:
                    self.conditions_sell.append({key: condition})

    @classmethod
    def save_db(cls, algorithm):
        try:
            print('update old algo')
            algo = Algorithms.objects.get(uuid=algorithm['uuid'])
            algo.user_id = algorithm['user_id']
            algo.name = algorithm['name']
            algo.uuid = algorithm['uuid']
            algo.json_string = json.dumps(algorithm)
            algo.save()
        except Algorithms.DoesNotExist:
            print('create new algo')
            algo = Algorithms.objects.create(
            user_id=algorithm['user_id'],
            name=algorithm['name'],
            uuid=algorithm['uuid'],
            json_string=json.dumps(algorithm))
        except Exception as e:
            print(e)
        finally: return algo
