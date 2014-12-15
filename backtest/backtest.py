## get contingencies
from calculator import *
from risk_calculator import *
from blocks import *
from conditions import *
from algorithm import BaseAlgorithm
from models import *

import math
import re
from datetime import date,timedelta


class BacktestingEnvironment:

    def __init__(self,backtest,algorithm):
        self.id = backtest['id']
        self.start_date = backtest['start_date']
        self.end_date = backtest['end_date']
        self.initial_balance = backtest['initial_balance']
        self.frequency = backtest['frequency']
        self.num_holdings = backtest['num_holdings']
    
        ## set up algorithm ##
        self.blocks_buy = algorithm['blocks_buy']
        self.blocks_sell = algorithm['blocks_sell']
        
        self.conditions_buy = {}
        self.conditions_sell = {}
        for condition in algorithm['conditions_buy']:
            self.conditions_buy[list(condition)[0]] = condition[list(condition)[0]]
        for condition in algorithm['conditions_sell']:
            self.conditions_sell[list(condition)[0]] = condition[list(condition)[0]]
        self.algorithm = algorithm['algorithm']
        
        ## relevant dates ##
        self.most_recent_trade = self.start_date
        self.dates_in_range = sorted(set(self.dates_in_range()))
        self.stocks_in_market = Stocks.objects.all()
        self.c = Calculator()
        self.portfolio = []
        self.balance = self.initial_balance
        self.latest_value = self.initial_balance

        ## risk calc
        self.market_index = [{'price': x.close, 'date': x.date} for x in Prices.objects.filter(stock_id=387).filter(date__range=(self.start_date, self.end_date)).order_by('date')]

        self.queue = None

    def set_queue(self, queue):
        self.queue = queue

    def dates_in_range(self):
        robust_stock = Stocks.objects.get(symbol='A')
        return [x.date for x in Prices.objects.filter(stock=robust_stock).filter(date__range=(self.start_date, self.end_date)).order_by('date')]

    ## main backtesting method ##
    def run_period_with_algorithm(self):
        for index,date in enumerate(self.dates_in_range):
            if index % math.floor(252/self.frequency) == 0:
                self.execute_trading_session(date)

                # calculate risk metrics

                value = round(PortfolioCalculator(self.portfolio).value,2)
                returns = round(float(((self.balance + value) - self.initial_balance) / self.initial_balance),2)

                ## Save returns
                # self.queue.enqueue({'key': 'returns', 'values': returns})

                self.print_information(date)
                if index > 0:
                    print(self.calculate_risk_metrics(self.most_recent_trade,date))
                # send portfolio to front end
                self.most_recent_trade = date
        return True

    ## helper method ##
    def execute_trading_session(self, date):
        ## sell based on conditions ##
        to_sell = self.sell_conditions(date)
        for asset in self.portfolio[:]:
            if len([1 for x in to_sell if x['symbol'] == asset['symbol']]) > 0:
                self.sell_stock(asset, date)
        
        ## buy based on conditions ##
        holdings = self.buy_conditions(date)
        if len(holdings) > 0:
            investment_per_stock = math.floor(self.balance / len(holdings))
            for stock in holdings:
                self.buy_stock(investment_per_stock, stock)
            
        ## Save State in DB ##
        # user_id = request.sessions['user_id']
        for asset in self.portfolio:
            stock = Stocks.objects.get(symbol=asset['symbol'])
            asset_db = {
                'algorithm' : self.algorithm,
                'stock' : stock,
                'quantity' : asset['quantity'],
                'price_purchased' : asset['price_purchased'],
                'date' : date,
            }
            Assets.objects.create(**asset_db)

        return True

    ## support methods ##
    def buy_stock(self,dollar_amount,stock):
        quantity = math.floor(dollar_amount / stock['todays_price'])
        if quantity > stock['todays_volume']*0.20:  ## can't exceed 20% of daily trading volume
            quantity = stock['todays_volume']*0.20
            dollar_amount = quantity*stock['todays_price']
        self.balance -= dollar_amount
        self.portfolio.append({
            'symbol' : stock['symbol'],
            'price_purchased' : stock['todays_price'],
            'quantity' : quantity,
            'object' : stock['object'],
            })
        return True

    def sell_stock(self,asset,date):
        yesterday = date - timedelta(days=1)
        price = list(Prices.objects.filter(stock=asset['object']).filter(date__range=(yesterday, date)))
        if len(price) > 0:
            sale = round((asset['quantity']*price[-1].close),2)
            self.balance += sale
            self.portfolio.remove(asset)
            return True
        return False

    ## Conditions ##
    def sell_conditions(self,date):
        portfolio = [x['object'] for x in self.portfolio]
        stocks_to_sell = [block.aggregate_stocks(portfolio,date) for block in self.blocks_sell]
        combined_stock_list = []
        for stock in stocks_to_sell:
            combined_stock_list += stock
        if len(self.blocks_sell) == 0:
            combined_stock_list =  self.portfolio
        for stock in combined_stock_list[:]:
            if stock is None:
                combined_stock_list.remove(stock)


        ranked_stocks = self.rank_stocks(combined_stock_list)
        survivors = Conditions(self.conditions_sell,ranked_stocks).aggregate_survivors()

        return sorted(survivors,key=(lambda x: x['agg_score']),reverse=True)

    def buy_conditions(self,date):
        stocks_to_buy = [block.aggregate_stocks(self.stocks_in_market,date) for block in self.blocks_buy]  
        combined_stock_list = []
        for block_return in stocks_to_buy:
            combined_stock_list += block_return ## concatenate lists
        for stock in combined_stock_list[:]:
            if stock is None:
                combined_stock_list.remove(stock)

        ranked_stocks = self.rank_stocks(combined_stock_list)
        ## purge stocks that don't meet conditions
        survivors = Conditions(self.conditions_buy,ranked_stocks).aggregate_survivors()
        
        return sorted(survivors,key=(lambda x: x['agg_score']),reverse=True)[:self.num_holdings]

    def rank_stocks(self,stock_array):
        ## rank stocks based on performance ## 
        for stock in stock_array:
            if stock is None:
                continue
            scores = []
            for point in [x for x in stock_array if x['symbol'] == stock['symbol']]:
                scores.append([point[key] for key in point if (key=='sma_score' or key == 'volatility_score' or key == 'covariance_score')])
            aggregate_score = 0
            for score in scores:
                if len(score) > 0:
                    aggregate_score += score[0]
            stock['agg_score'] = aggregate_score
        return stock_array

    def calculate_risk_metrics(self,previous_trade,date):
        value = round(PortfolioCalculator(self.portfolio).value,2)
        rmc = RiskMetricsCalculator(self.portfolio,self.balance,self.initial_balance,self.market_index,previous_trade,date)
        return {
            'alpha': rmc.alpha(), 
            'beta': rmc.beta(), 
            'sharpe': rmc.sharpe(), 
            'volatility': rmc.volatility(), 
            'returns': rmc.total_returns()
            }

    ## Views ##
    def print_information(self,date):
        print("------------------------------------------------")
        print("Date : ",date)
        for asset in self.portfolio:
            line = "Stock : " + asset['symbol'] + ', quantity : ' + str(asset['quantity']) + ', at : ' + str(asset['price_purchased'])
            print(line)
        print("Balance : ",round(self.balance,2))
        value = round(PortfolioCalculator(self.portfolio).value,2)
        print("Portfolio Value : ",value)
        return True

    def run(self):
        self.run_period_with_algorithm()


## Script ##
if __name__ == '__main__':
    ## at this point, back end expects a JSON
    json = {
        'backtest': {
            'id' : 'asjdlfakjdfl;akjdl;fajkd;fadfa',
            'start_date': "2013-01-01",
            'end_date': "2014-01-01",
            'initial_balance': 1000000,
            'frequency': 12,
            'num_holdings': 2,
            }, 
        'algorithm': {
            'name' : 'Test',
            'block': {
                'sma': {
                    'buy': [{
                        'period1': 15, 
                        'period2': 10,
                        'range': (0.2,10),
                        'appetite': 5
                        },{
                        'period1': 2, 
                        'period2': 50,
                        'range': (0.8,10),
                        'appetite': 50
                        }],
                    'sell' : []
                },
                'volatility' : {
                    'buy' : [],
                    'sell' : [{
                        'behavior': 'sell', # or sell
                        'period': 15,
                        'appetite': 100,
                        'range': (0.1,0.2),
                        }] 
                },
                'covariance': {
                    'buy' :[{
                        'benchmark': 'ACE',
                        'period': 15,
                        'appetite': 200,
                        'range': (0.1,0.2,),
                    }],
                    'sell' : []
                },
                'thresholds': {
                    'buy' :[{
                        'price' : {'above': 50, 'below': 100},
                        # 'sector' : {'include': ['Healthcare']},
                        # 'industry': {'exclude': ['Asset Management']}
                        }],
                    'sell' : []
                },
                'diversity': {
                    'buy' : [],
                    'sell' : [{
                        'num_sector': 2,
                        'num_industry': 1
                        }]
                },
                'event': {
                    'buy': [{
                        'stock': 'GOOG',
                        'attribute': 'close',
                        'range': (600,650,),
                        'appetite': 300
                        }],
                    'sell': []
                },
            }
        }
    }

    base = BaseAlgorithm(json['algorithm'])
    BacktestingEnvironment(json['backtest'], base.__dict__).run()

