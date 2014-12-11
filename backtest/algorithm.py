
## Algorithms built from Blocks ##

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
            'period1' : 'Null',
            'period2' : 'Null',
            'percent_difference_to_buy' : 'Null',
            'percent_difference_to_sell' : 'Null',
            'appetite' : 0,
        }
        self.volatility = {
            'period' : 'Null',
            'threshold_to_buy' : 'Null',
            'threshold_to_sell' : 'Null', 
            'appetite' : 0,
        }
        self.covariance = {
            'benchmark' : 'Null',
            'period' : 'Null',
            'desired' : {'above' : 'Null', 'below' : 'Null'},
            'threshold_to_sell' : 'Null',
            'appetite' : 0,
        }
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
        self.sma_block = {
            'status' : 'off',
            'class' : SMA_Block(**self.sma),
        }
        self.volatility_block = {
            'status' : 'off',
            'class' : Volatlity_Block(**self.volatility)
        }

        self.covariance_block = {
            'status' : 'off',
            'class' : Covariance_Block(**self.covariance)
        }

        self.diversity_condition = {
            'status' : 'off',
            'attributes' : self.diversity
        }
        self.threshold_condition = {
            'status' : 'off',
            'attributes' : self.thresholds
        }
        self.crisis_condition = {
            'status' : 'off',
            'attributes' : self.crisis
        }


    def __run__(self):
        be = BacktestingEnvironment(**self.__dict__)
        be.run_period_with_algorithm()
