
## Algorithms built from Blocks ##
from blocks import *

class BaseAlgorithm:

    def __init__(self,**kwargs):

        #### SET DEFAULTS ####

        ## Testing Environment ##
        self.testing_environment = {
            'start_date' : "2013-01-01",
            'end_date' : "2014-01-01",
            'initial_balance' : 1000000,
            'frequency' : 12,
            'num_holdings' : 3,
        }

        ## Sample Blocks Attributes ##
        self.sma = {
            'period1' : 0,
            'period2' : 0,
            'percent_difference_to_buy' : 'Null',
            'percent_difference_to_sell' : 'Null',
            'appetite' : 0,
        }
        self.volatility = {
            'period' : 0,
            'threshold_to_buy' : 'Null',
            'threshold_to_sell' : 'Null', 
            'appetite' : 0,
        }
        self.covariance = {
            'benchmark' : 'GOOG',
            'period' : 0,
            'desired' : {'above' : 'Null', 'below' : 'Null'},
            'threshold_to_sell' : 'Null',
            'appetite' : 0,
        }
        ## Conditions ## 

        self.diversity = {
            'num_sector' : 99999999, ## can't exeed threshold in portfolio
            'num_industry' : 99999999, ## e.g. 2 --> can't have more than 2 of same industry
        }
        self.thresholds = {
            'price' : {'above' : 0, 'below' : 9999999999},
            'sector' : {'include' : 'Null', 'exclude' : 'Null'},
            'industry' : {'include' : 'Null', 'exclude' : 'Null'}
        }
        self.crisis = {
            'percent_decline' : 0,
            'behavior' : 'Null' ## Hold, Sell All, diversify..
        }

        ## Overwrite Defaults ##
        for key in kwargs:
            setattr(self,key,kwargs[key])

        ## Encapsulate Blocks for Processing ##
        if 'sma' in kwargs:
            self.sma_block = {
                'status' : 'on',
                'class' : SMA_Block(**self.sma),
            }
        else:
            self.sma_block = {
                'status' : 'off'
            }

        if 'volatility' in kwargs:
            self.volatility_block = {
                'status' : 'on',
                'class' : Volatility_Block(**self.volatility)
            }
        else:
            self.volatility_block = {
                'status' : 'off'
            }

        if 'covariance' in kwargs:
            self.covariance_block = {
                'status' : 'on',
                'class' : Covariance_Block(**self.covariance)
            }
        else:
            self.covariance_block = {
                'status' : 'off'
            }

        if 'diversity' in kwargs:
            self.diversity_condition = {
                'status' : 'on',
                'attributes' : self.diversity
            }
        else:
            self.diversity_condition = {
                'status' : 'off'
            }

        if 'threshold' in kwargs:
            self.threshold_condition = {
                'status' : 'on',
                'attributes' : self.thresholds
            }
        else:
            self.threshold_condition = {
                'status' : 'off'
            }

        if 'crisis' in kwargs:
            self.crisis_condition = {
                'status' : 'on',
                'attributes' : self.crisis
            }
        else:
            self.crisis_condition = {
                'status' : 'off'
            }
