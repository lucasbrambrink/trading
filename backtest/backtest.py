## set up django
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()


## get contingencies
from calculator import *
from blocks import *
from models import Stocks,Prices
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
        self.dates_in_range = ParseDates().dates_in_range(self.start_date, self.end_date)
        self.stocks_in_market = Stocks.objects.all()
        self.c = Calculator()
        self.portfolio = []
        self.balance = self.initial_balance


    ## main backtesting method ##
    def run_period_with_algorithm(self):
        for index,date in enumerate(self.dates_in_range):
            if index % math.floor(365/self.frequency) == 0:
                self.execute_trading_session(date)
                self.print_information(date)
        return True

    ## helper method ##
    def execute_trading_session(self,date):
        stocks_to_buy = self.find_stocks_to_buy(date)

        ## sell first ##
        for asset in self.portfolio:
            stock = Stocks.objects.get(symbol=asset['symbol'])
            self.sell_stock(stock,date)

        ## buy stocks based on portfolio customization ##
        holdings = sorted(stocks_to_buy,key=(lambda x: x['pd']),reverse=True)[:self.holdings]
        investment_per_stock = math.floor(self.balance / len(holdings))
        for stock in holdings:
            self.buy_stock(investment_per_stock,stock['symbol'],date)
        
        ## Save Portfolio State in DB ##
        # user_id = request.sessions['user_id']
        portfolio_object = Portfolios.objects.get(user_id=user_id)
        for asset in self.portfolio:
            stock = Stocks.objects.get(symbol=asset['symbol'])
            asset_db = {
                'portfolio' : portfolio_object,
                'stock' : stock,
                'quantity' : asset['quantity'],
                'price_purchased' : asset['price_purchased'],
                'date' : date,
            }
            Asset.objects.create(**asset_db)

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
            if block['status'] != "off":
                stocks_to_buy.append(block['class'].aggregate_stocks())
        
        survivors = Conditions(self.conditions,stocks_to_buy).aggregate_survivors()
        ## now rank survivors 
        scored_survivors = []
        for survivor in survivors:
            mult = [x for x in survivors if x['symbol'] == survivor['symbol']]
            sma_score,volatility_score,covariance_score = 0,0,0
            for point in mult:
                sma_score = [self.sma['appetite']*point[key] for key in point if key=='pd'][0]
                volatility_score = [self.volatility['appetite']*point[key] for key in point if key == 'vol'][0]
                covariance_score = [self.covariance['appetite']*point[key] for key in point if key == 'covariance'][0]
            survivor['agg_score'] = sma_score + volatility_score + covariance_score
            scored_survivors.append(survivor)
        return sorted(scored_survivors,key=(lambda x: x['agg_score'],reverse=True)[:self.holdings]


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



## Script ##
if __name__ == '__main__':
    ## at this point, back end expects a JSON
    json = {'sma_period' : 15, 'sma_percent_difference_to_buy':0.1}
    base = BaseAlgorithm(**json) ## 15 day SMA for 0.1 percent difference to buy
    base.__run__()
    




