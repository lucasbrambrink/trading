## set up django
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()


## get contingencies
from calculator import *
from models import Stocks,Prices
import math

## Helper Class
class ParseDates:

    def __init__(self):
        self.prepare_dates_for_data_collection()

    def prepare_dates_for_data_collection(self):
        """
        Generate a list of dates in the format of "yyyy-mm-dd" from 2000-01-01 to 2013-12-31

        :return: date list
        """
        self.all_dates = []
        for year in range(2000, 2014):
            for month in range(1,13):
                for day in range(1,32): ## it is okay for all months to go to 31 bc many of the dates wont be in the DB regardless (stock market closed)
                    date_str = "{y}-{m:0=2d}-{d:0=2d}".format(y=year, m=month, d=day)
                    self.all_dates.append(date_str)

    @staticmethod
    def split_date_into_ints(date):
        """
        Split date string into (year, month, day) integers

        params: date = "yyyy-mm-dd"
        returns: (year, month, day) integers
        """
        return map(lambda x: int(x), date.split('-'))

    @staticmethod
    def dates_in_range(start_date,end_date):
        stock = Stocks.objects.filter(symbol='GOOG')
        dates = Prices.objects.filter(stock=stock).filter(date__range(start_date,end_date))
        return [date.date for date in dates]


class BacktestingEnvironment:

    def __init__(self,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])

        ## relevant dates ##
        self.dates_in_range = ParseDates().dates_in_range(self.start_date, self.end_date)
        self.stocks_in_market = Stocks.objects.all()
        self.c = Calculator()
        self.portfolio = []
        self.balance = self.initial_balance


    ## main backtesting method ##
    def run_period_with_algorithm(self):
        print('run algorithm')
        for index,date in enumerate(self.dates_in_range):
            if index % math.floor(365/self.frequency) == 0:
                self.execute_trading_session(date)
                self.print_information(date)
        return True

    ## helper method ##
    def execute_trading_session(self,date):
        print('executing trading session, date: ',date)
        stocks_to_buy = self.find_stocks_to_buy(date)
        if len(stocks_to_buy) == 0:
            return False

        ## sell first ##
        for asset in self.portfolio:
            stock = Stocks.objects.get(symbol=asset['symbol'])
            self.sell_stock(stock,date)

        ## buy stocks based on portfolio customization ##
        holdings = sorted(stocks_to_buy,key=(lambda x: x['pd']),reverse=True)[:self.holdings]
        investment_per_stock = math.floor(self.balance / len(holdings))
        for stock in holdings:
            self.buy_stock(investment_per_stock,stock['symbol'],date)
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

    def get_sma_pair_per_stock(self,date,stock_object):
        sma1_prices = []
        sma2_prices = []
        start_id = Prices.objects.filter(stock=stock_object).filter(date=date)
        if len(start_id) > 0:
        	start_id = start_id[0].id
        else:
        	return {'symbol' : 'ZZZ', 'sma_pair' : (1,1,), 'date' : date,}
        ## DB is seeded backwards (starts with latest date)
        end_id = start_id + (self.sma_period * 2) ## pair
        prices_in_range = Prices.objects.filter(id__range=(start_id,end_id))
        for index,price in enumerate(prices_in_range[::-1]): ## arrange into proper order
            if len(prices_in_range[index].close) == 0:
                continue 
            if index < (len(prices_in_range)/2):
                sma1_prices.append({'price' : float(prices_in_range[index].close),'date' : date })
            else:
                sma2_prices.append({'price' : float(prices_in_range[index].close),'date' : date })
        sma1 = self.c.average(sma1_prices,'price')
        sma2 = self.c.average(sma2_prices,'price')
        sma_pair = {
            'symbol' : stock_object.symbol,
            'sma_pair' : (sma1,sma2,),
            'date' : date,
            'close' : prices_in_range[0].close,
            'object' : stock_object
            }
        return sma_pair


    ## this needs to be encapsulated further ##
    def find_stocks_to_buy(self,date):
        stocks_to_buy = []  
        if self.sma_period != 'Null':
            all_stock_sma_pairs = [self.get_sma_pair_per_stock(date,stock_object) for stock_object in self.stocks_in_market]
            for pair in all_stock_sma_pairs:
                pd = self.c.percent_change_simple(pair['sma_pair'][1],pair['sma_pair'][0])
                if pd > self.sma_percent_difference_to_buy:
                    stocks_to_buy.append({
                        'symbol' : pair['symbol'],
                        'pd' : pd,
                        'price' : pair['close'],
                        'object' : pair['object']
                        })
        if self.volatility != 'Null':
            pass
        # etc.
        ## other blocks run their conditions
        

        ## now throw out ones that don't pass threshold ##
        ## i think it's easiest to do now rather than add into every block logic  

        for stock in stocks_to_buy:
            for key,value in self.threshold_price:
                if (key == 'below' and value > stock['price'] or
                    key == 'above' and value < stock['price']):
                    stocks_to_buy.remove(stock)
                    break
            if (stock['object'].sector in self.threshold_sector or
                stock['object'].industry in self.threshold_industry):
                    stocks_to_buy.remove(stock)
                    break
        return stocks_to_buy

        


        return stocks_to_buy

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


## Algorithms built from Blocks ##

class SampleAlgorithm:
## marks stocks whose 30 day SMA (simple moving average) has changed by more than 10%

    def __init__(self,**kwargs):

        #### SET DEFAULTS ####

        ## Testing Environment ##
        self.start_date = "2013-01-01"
        self.end_date = "2014-01-01"
        self.initial_balance = 1000000

        ## Frequency ##
        self.frequency = 12 ## represent as times per year the code should execute

        ## Customize Portfolio
        self.number_of_holdings = 3

        ## Sample Blocks ##
        self.sma_period = "Null"
        self.sma_percent_difference_to_buy = "Null"
        self.sma_percent_difference_to_sell = "Null"
        
        self.sma_volatility = "Null"
        self.sma_volatility_threshold = "Null"

        ## Threshold Contions ##
        self.threshold_price = "Null" ## {'below' : 500,'above' : 200}
        self.threshold_sector = "Null" ## {'yes' : 'healthcare'}
        self.threshold_industry = "Null" ## {'yes' : 'biotechnology'}

        ## Crisis Conditions ##
        self.crisis_threshold = "Null"
        ## could be general downturn in market (all sma's get calculated)

        for key in kwargs:
            setattr(self,key,kwargs[key])

        ## Ideas ##
        # - volatility of stock below certain threshold
        # - limit scope on sector / industry
        # - all other economic data can be used (P/E,R/E,...)
        # - covariance of sectors, industries --> aim for diversity in stocks
        # - covariance of stocks to each other --> avoid holding on to similar covariances in portfolio
        # - different parameter with averages
        #############

    def __run__(self):
        be = BacktestingEnvironment(**self.__dict__)
        be.run_period_with_algorithm()



## Script ##
if __name__ == '__main__':
    ## at this point, back end expects a JSON
    json = {'sma_period' : 15, 'sma_percent_difference_to_buy':0.1}
    sa = SampleAlgorithm(**json) ## 15 day SMA for 0.1 percent difference to buy
    sa.__run__()
    




