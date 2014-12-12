
## Algorithms built from Blocks ##
from blocks import *
from models import Algorithms

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
            'threshold_to_buy': 'Null',
            'threshold_to_sell': 'Null', 
            'appetite': 0,
        }
        self.covariance = {
            'benchmark': 'GOOG',
            'period': 0,
            'desired': {'above' : 'Null', 'below' : 'Null'},
            'threshold_to_sell': 'Null',
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
        if 'sma' in algorithm:
            self.sma_block = SMA_Block(**self.sma)

        if 'volatility' in algorithm:
            self.volatility_block = Volatility_Block(**self.volatility)
    
        if 'covariance' in algorithm:
            self.covariance_block = Covariance_Block(**self.covariance)
        
        if 'diversity' in algorithm:
            self.diversity_condition = self.diversity
    
        if 'threshold' in algorithm:
            self.threshold_condition = self.thresholds
            
        if 'crisis' in algorithm:
            self.crisis_condition = self.crisis

        self.algorithm = self.save_db()

    def save_db(self):
        a = Algorithms.objects.create(name=self.name)
        return a
           
