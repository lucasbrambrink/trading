## set up django
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()


## get contingencies
from calculator import *
from models import Stocks,Prices
import math


## Helper Class
class CollectData:

    @staticmethod
    def market_snapshot_by_date(date):
        all_stocks = Prices.objects.filter(date=date)
        day = {'date': date, 'data': all_stocks}
        return day

    @staticmethod
    def market_snapshot_by_stock(symbol):
        stock = Stocks.objects.get(symbol=symbol)
        all_prices = Prices.objects.filter(stock=stock)
        stock = {'symbol': symbol, 'data': all_prices}
        return stock

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
    def compare_two_dates(date1, date2):
        """
        Compare dates in chronological order.

        :param date1: date string
        :param date2: date string
        :return: -1 if date1 is smaller than date2. 0 equals. 1 date1 is larger than date2.
        """
        y1, m1, d1 = ParseDates.split_date_into_ints(date1)
        y2, m2, d2 = ParseDates.split_date_into_ints(date2)

        if y1 > y2:
            return 1
        elif y1 < y2:
            return -1
        else:
            if m1 > m2:
                return 1
            elif m1 < m2:
                return -1
            else:
                if d1 > d2:
                    return 1
                elif d1 < d2:
                    return -1
                else:
                    return 0

    def collect_dates_in_range(self, start_date, end_date):
        """
        Return a list of dates between start_date and end_date

        :param start_date: date string
        :param end_date: date string
        :return: a list of date string
        """
        data_len = len(self.all_dates)
        lower_bound = 0
        if ParseDates.compare_two_dates(self.all_dates[0], start_date) < 0:
            # start_date is larger than the first date in database
            # Look for lower bound
            l = 0
            r = data_len-1
            while l < r:
                mid = int((r - l) / 2) + l
                if ParseDates.compare_two_dates(self.all_dates[mid], start_date) == 0:
                    lower_bound = mid
                    break
                elif ParseDates.compare_two_dates(self.all_dates[mid], start_date) > 0:
                    r = mid-1
                else:
                    l = mid+1
            if ParseDates.compare_two_dates(self.all_dates[l], start_date) >= 0:
                lower_bound = l
            else:
                lower_bound = l+1

        upper_bound = data_len-1
        if ParseDates.compare_two_dates(self.all_dates[data_len-1], end_date) > 0:
            # end_date is smaller than the last date in database
            # Look for upper bound
            l = 0
            r = data_len-1
            while l < r:
                mid = int((r - l) / 2) + l
                if ParseDates.compare_two_dates(self.all_dates[mid], end_date) == 0:
                    upper_bound = mid
                    break
                elif ParseDates.compare_two_dates(self.all_dates[mid], end_date) > 0:
                    r = mid-1
                else:
                    l = mid+1
            if l == r:
                if ParseDates.compare_two_dates(self.all_dates[l], end_date) <= 0:
                    upper_bound = l
                else:
                    upper_bound = l-1

        print(lower_bound)
        print(upper_bound)
        return self.all_dates[lower_bound:upper_bound+1]


class BacktestingEnvironment:

    def __init__(self,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])

        ## relevant dates ##
        self.dates_in_range = ParseDates().collect_dates_in_range(self.start_date, self.end_date)
        self.stocks_in_market = Stocks.objects.all()
        self.c = Calculator()
        self.portfolio = []
        self.balance = self.initial_balance


    ## main backtesting method ##
    def run_period_with_algorithm(self):
        print('run algorithm')
        portfolio = []
        index = 0
        while index < len(self.dates_in_range):
            date = self.dates_in_range[index]
            year,month,day = ParseDates.split_date_into_ints(date)
            if month > 2: ## range for days to go back
                if day < 5:
                    ## test if it's a proper trading day
                    sample = Prices.objects.filter(date=date)
                    if len(sample) == 0:
                        index += 1
                    else:
                        ## wont repeat more than once
                        self.execute_trading_session(date)
                        self.print_information(date)
                        index += 15 ## ensures if condition won't be met twice per month
            index += 1
        return True

    ## helper method ##
    def execute_trading_session(self,date):
        print('executing trading session, date: ',date)
        stocks_to_buy = self.find_stocks_to_buy(date)

        ## sell everything in portfolio first ( just do it )
        for asset in self.portfolio:
            stock = Stocks.objects.get(symbol=asset['symbol'])
            self.sell_stock(stock,date)

        ## now buy stocks 
        ## rank their SMA pd's
        best_three = sorted(stocks_to_buy,key=(lambda x: x['pd']),reverse=True)[:3]
        ## equally divide holdings to all three
        if len(best_three) == 0:
        	return False
        investment_per_stock = math.floor(self.balance / len(best_three))
        for stock in best_three:
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

    def get_sma_pair_previous_2_periods(self,date):
        print('get previous 2 smas')
        all_stock_sma_pairs = []
        date_specific_index = self.dates_in_range.index(date)
        for stock_object in self.stocks_in_market:
            all_stock_sma_pairs.append(self.get_sma_pair_per_stock(date,stock_object))
        return all_stock_sma_pairs

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
            }
        return sma_pair

    def find_stocks_to_buy(self,date):
        print('determining stocks to match sma threshold')
        all_stock_sma_pairs = self.get_sma_pair_previous_2_periods(date)
        stocks_to_buy = []
        for pair in all_stock_sma_pairs:
            pd = self.c.percent_change_simple(pair['sma_pair'][1],pair['sma_pair'][0])
            if pd > self.sma_percent_difference_to_buy:
                stocks_to_buy.append({
                    'symbol' : pair['symbol'],
                    'pd' : pd
                    })
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


        ## Sample Blocks ##
        self.sma_period = "Null"
        self.sma_percent_difference_to_buy = "Null"
        self.sma_percent_difference_to_sell = "Null"
        
        self.sma_volatility = "Null"
        self.sma_volatility_threshold = "Null"

        ## Threshold Contions ##
        self.price = "Null"
        self.sector = "Null"
        self.industry = "Null"

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
    




