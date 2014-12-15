
## Algorithms built from Blocks ##
from blocks import *
from models import Algorithms
import re

class BaseAlgorithm:

    def __init__(self,algorithm):

        for key in algorithm:
            if key == 'name':
                setattr(self,key,algorithm[key])
            if key == 'sma':
                self.sma_blocks_buy = [SMA_Block(**condition) for condition in algorithm[key] if condition['behavior'] == 'buy']
                self.sma_blocks_sell = [SMA_Block(**condition) for condition in algorithm[key] if condition['behavior'] == 'sell']
            if key == 'volatility':
                self.volatility_blocks_buy = [Volatility_Block(**condition) for condition in algorithm[key] if condition['behavior'] == 'buy']
                self.volatility_blocks_sell = [Volatility_Block(**condition) for condition in algorithm[key] if condition['behavior'] == 'sell']
            if key == 'covariance':
                self.covariance_blocks_buy = [Covariance_Block(**condition) for condition in algorithm[key] if condition['behavior'] == 'buy']
                self.covariance_blocks_sell = [Covariance_Block(**condition) for condition in algorithm[key] if condition['behavior'] == 'sell']
            if key == 'event':
                self.event_blocks_buy = [Event_Block(**condition) for condition in algorithm[key] if condition['behavior'] == 'buy']
                self.event_blocks_sell = [Event_Block(**condition) for condition in algorithm[key] if condition['behavior'] == 'sell']
            if key == 'diversity':
                self.diversity_conditions_buy = [condition for condition in algorithm[key] if condition['behavior'] == 'buy']
                self.diversity_conditions_sell = [condition for condition in algorithm[key] if condition['behavior'] == 'sell']
            if key == 'thresholds':
                self.thresholds_conditions_buy = [condition for condition in algorithm[key] if condition['behavior'] == 'buy']
                self.thresholds_conditions_sell = [condition for condition in algorithm[key] if condition['behavior'] == 'sell']
            if key == 'crisis':
                self.crisis_conditions = [condition for condition in algorithm[key]]


        self.algorithm = self.save_db()

    def save_db(self):
        a = Algorithms.objects.create(name=self.name)
        return a
           
