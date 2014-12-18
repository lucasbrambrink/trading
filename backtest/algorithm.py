
## Algorithms built from Blocks ##
from blocks import *
from models import Algorithms
import re
import json

class BaseAlgorithm:

    def __init__(self,algorithm):
        self.blocks_buy = []
        self.blocks_sell = []
        self.conditions_buy = []
        self.conditions_sell = []
        setattr(self,'name',algorithm['name'])
        setattr(self,'uuid',algorithm['uuid'])
        setattr(self,'json_string',json.dumps(algorithm))
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

        self.algorithm = self.save_db()

    def save_db(self):
        a = Algorithms.objects.create(
            user_id=1,
            name=self.name,
            uuid=self.uuid,
            json_string=self.json_string)
        return a
           
