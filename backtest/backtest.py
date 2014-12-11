## set up django
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()


## get contingencies
from calculator import *
from blocks import *
from conditions import *
from algorithm import BaseAlgorithm
from models import Stocks,Prices,Portfolios,Assets
import math
import re



class BacktestingEnvironment:

    def __init__(self,**kwargs):
        self.blocks = []
        self.conditions = {}
        for key in kwargs:
            if key == 'testing_environment':
                for attr in kwargs[key]:
                    setattr(self,attr,kwargs[key][attr])
            if re.search('_block',key):
                self.blocks.append(kwargs[key])
            if re.search('_condition',key):
                short_key = key.split('_')[0]
                self.conditions[short_key] = kwargs[key]

        ## relevant dates ##
        self.dates_in_range = self.dates_in_range()
        self.stocks_in_market = Stocks.objects.all()
        self.c = Calculator()
        self.portfolio = []
        self.balance = self.initial_balance

    def dates_in_range(self):
        robust_stock = Stocks.objects.get(symbol='ACE')
        return [x.date for x in Prices.objects.filter(stock=robust_stock).filter(date__range=(self.start_date,self.end_date))]

    ## main backtesting method ##
    def run_period_with_algorithm(self):
        for index,date in enumerate(self.dates_in_range):
            if index % math.floor(365/self.frequency) == 0:
                self.execute_trading_session(date)
                ## send portfolio to front end
                self.print_information(date)
        return True

    ## helper method ##
    def execute_trading_session(self,date):
        ## sell first ##
        for asset in self.portfolio:
            stock = Stocks.objects.get(symbol=asset['symbol'])
            self.sell_stock(stock,date)

        ## buy stocks based on portfolio customization ##
        holdings = self.find_stocks_to_buy(date)
        investment_per_stock = math.floor(self.balance / len(holdings))
        for stock in holdings:
            self.buy_stock(investment_per_stock,stock['symbol'],date)
        
        ## Save Portfolio State in DB ##
        # user_id = request.sessions['user_id']
        # portfolio_object = Portfolios.objects.get(user=user_id)
        # for asset in self.portfolio:
        #     stock = Stocks.objects.get(symbol=asset['symbol'])
        #     asset_db = {
        #         'portfolio' : portfolio_object,
        #         'stock' : stock,
        #         'quantity' : asset['quantity'],
        #         'price_purchased' : asset['price_purchased'],
        #         'date' : date,
        #     }
        #     Assets.objects.create(**asset_db)

        return True

    ## support methods ##
    def buy_stock(self,dollar_amount,symbol,date):
        stock = Stocks.objects.get(symbol=symbol)
        price = Prices.objects.filter(stock=stock).filter(date=date)
        if len(price) > 0:
            quantity = math.floor(dollar_amount / float(price[0].close))
            self.balance -= dollar_amount
            self.portfolio.append({
                'symbol' : stock.symbol,
                'price_purchased' : float(price[0].close),
                'quantity' : quantity
                })
            print(dollar_amount,': ',quantity," of ",stock.symbol," for ",price[0].close)
            return True
        else:
            return False # unable to buy for this date

    def sell_stock(self,stock,date):
        price = Prices.objects.filter(stock=stock).filter(date=date)
        if len(price) > 0:
            asset = [x for x in self.portfolio if x['symbol'] == stock.symbol][0]
            sale = round((asset['quantity']*float(price[0].close)),2)
            self.balance += sale
            self.portfolio.remove(asset)
            print(sale,": ",asset['symbol']," for ",price[0].close)
            return True
        else:
            return False


    ## this needs to be encapsulated further ##
    def find_stocks_to_buy(self,date):
        stocks_to_buy = []  
        for block in self.blocks:
            if block['status'] == "on":
                # print(block['class'])
                stocks_to_buy.append(block['class'].aggregate_stocks(self.stocks_in_market,date))
        
        survivors = Conditions(self.conditions,stocks_to_buy).aggregate_survivors()[0]
        ## now rank survivors 
        scored_survivors = []
        print(survivors)
        for survivor in survivors:
            mult = [x for x in survivors if x['symbol'] == survivor['symbol']]
            scores = []
            for point in mult:
                scores.append([point[key] for key in point if (key=='sma_score' or key == 'volatility_score' or key == 'covariance_score')])
            aggregate_score = 0
            for score in scores:
                if len(score) > 0:
                    aggregate_score += score[0]
            survivor['agg_score'] = aggregate_score
            scored_survivors.append(survivor)
        return sorted(scored_survivors,key=(lambda x: x['agg_score']),reverse=True)[:self.num_holdings]


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
        returns = round(float(((self.balance + value) - self.initial_balance) / self.initial_balance),2)
        print("Returns : ",returns)
        return True

    def __run__(self):
        self.run_period_with_algorithm()


## Script ##
if __name__ == '__main__':
    ## at this point, back end expects a JSON
    json = { 'backtest' : {}, 'algorithm' : [ ] } 


    'sma' : {
        'period1' : 15, 
        'period2' : 10,
        'percent_difference_to_buy':0.1,
        'appetite' : 5}
        }
    base = BaseAlgorithm(**json)
    BacktestingEnvironment(**base.__dict__).__run__()



