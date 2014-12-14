
## Algorithms built from Blocks ##
from blocks import *
from models import Algorithms
import re

class BaseAlgorithm:

    def __init__(self,algorithm):

        #### SET DEFAULTS ####

        ## Sample Blocks Attributes ##

        self.sma = {
            'period1': 0,
            'period2': 0,
            'percent_difference_to_buy': 'Null',
            'percent_difference_to_sell': 'Null',
            'appetite': 0,
        }
        self.volatility = {
            'period': 0,
            'range': (0,0,),
            'appetite': 0,
        }
        self.covariance = {
            'benchmark': 'ACE',
            'period': 0,
            'range': (0,0,),
            'appetite': 0,
        }
        ## Conditions ## 

        self.diversity = {
            'num_sector': 99999999, ## can't exeed threshold in portfolio
            'num_industry': 99999999, ## e.g. 2 --> can't have more than 2 of same industry
        }
        self.thresholds = {
            'price': {'above': 0, 'below': 9999999999},
            'sector': {'include': 'Null', 'exclude': 'Null'},
            'industry': {'include': 'Null', 'exclude': 'Null'}
        }
        self.crisis = {
            'percent_decline': 0,
            'behavior': 'Null' ## Hold, Sell All, diversify..
        }

        ## Overwrite Defaults ##
        for key in algorithm:
            setattr(self,key,algorithm[key])

        ## Encapsulate Blocks for Processing ##
        self.sma_blocks_buy = [SMA_Block(getattr(self,condition)) for condition in [key for key in algorithm if re.search('sma',key)] if condition['behavior'] == 'buy']
        self.sma_blocks_sell = [SMA_Block(getattr(self,condition)) for condition in [key for key in algorithm if re.search('sma',key)] if condition['behavior'] == 'buy']
            
        self.volatility_blocks_buy = [Volatility_Block(getattr(self,condition)) for condition in [key for key in algorithm if re.search('volatility',key)] if condition['behavior'] == 'buy']
        self.volatility_blocks_sell = [Volatility_Block(getattr(self,condition)) for condition in [key for key in algorithm if re.search('volatility',key)] if condition['behavior'] == 'sell']
        
        self.covariance_blocks_buy = [Covariance_Block(getattr(self,condition)) for condition in [key for key in algorithm if re.search('covariance',key)] if condition['behavior'] == 'buy']
        self.covariance_blocks_sell = [Covariance_Block(getattr(self,condition)) for condition in [key for key in algorithm if re.search('covariance',key)] if condition['behavior'] == 'buy']
            
        self.diversity_conditions_buy = [getattr(self,condition) for condition in [key for key in algorithm if re.search('diversity',key)] if condition['behavior'] == 'buy']
        self.diversity_conditions_sell = [getattr(self,condition) for condition in [key for key in algorithm if re.search('diversity',key)] if condition['behavior'] == 'sell']
        
        self.thresholds_conditions_buy = [getattr(self,condition) for condition in [key for key in algorithm if re.search('sma',key)] if condition['behavior'] == 'buy']
        self.thresholds_conditions_sell = [getattr(self,condition) for condition in [key for key in algorithm if re.search('sma',key)] if condition['behavior'] == 'buy']
            
        self.crisis_conditions = [getattr(self,condition) for condition in [key for key in algorithm if re.search('crisis',key)]]

        self.algorithm = self.save_db()

    def save_db(self):
        a = Algorithms.objects.create(name=self.name)
        return a
           
