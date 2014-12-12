import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graph_trader.settings.dev")
django.setup()

from calculator import *
from models import Stocks,Prices



class PortfolioReturns:

    def __init__(self,portfolio,initial_balance,start_date,end_date,market_returns):
        self.portfolio = portfolio
        self.initial_balance = initial_balance
        self.start_date = start_date
        self.end_date = end_date
        self.market_returns = market_returns

    def update(self):
        dates = [{'date': x.date, 'data': []} for x in Prices.objects.filter(stock_id=387).filter(date__range=(self.start_date,self.end_date)).order_by('date')]
        # print(dates)
        for asset in self.portfolio:
            prices = Prices.objects.filter(stock=asset['object']).filter(date__range=(self.start_date,self.end_date)).order_by('date')
            price_dict = {}
            for price in prices:
                price_dict[price.date] = price.close
            for date in dates:
                date['data'].append({'quantity': asset['quantity'], 'price': price_dict[date['date']]})
        for date in dates:
            daily_value = 0
            for asset in date['data']:
                daily_value += asset['quantity']*asset['price']
            daily_return = round(float((daily_value - self.initial_balance)/self.initial_balance),4)
            date['value'] = daily_value
            date['returns'] = daily_return
            market_returns = [x['returns'] for x in self.market_returns if x['date'] == date['date']]
            if len(market_returns) == 0:
                market_returns = [x.returns for x in self.market_returns if x.date == dates[dates.index(date)-1]['date']]
            if len(market_returns) == 0:
                market = 0
            else:
                market = market_returns[-1]
            date['market_returns'] = market
        return dates


class RiskMetricsCalculator:

    def __init__(self,portfolio,market_index,start_date,end_date):
        self.portfolio = portfolio
        self.market_index = market_index
        self.start_date = start_date
        self.end_date = end_date
        self.value = self.value()
        ## update
        self.update_values()
        self.risk_free = Prices.objects.filter(stock_id=388).filter(date__range=(self.start_date,self.end_date)).order_by('date')
        self.market_returns = Calculator.percent_change_array(self.market_index, 'price')
        ## contains all information
        self.date_master_list = PortfolioReturns(self.portfolio, self.value, self.start_date, self.end_date, self.market_returns).update()
        # print(self.date_master_list)
        self.c_portfolio_returns,self.c_market_returns = self.complementary_arrays()


    def value(self):
        """
        :return: float
        """
        value_portfolio = 0
        for asset in self.portfolio:
            value_portfolio += (asset['price_purchased']*asset['quantity'])
        return value_portfolio

    def update_values(self):
        for asset in self.portfolio:
            current_price = Prices.objects.filter(stock=asset['object']).filter(date=self.end_date)
            if len(current_price) > 0:
                returns = round(float((current_price[0].close - asset['price_purchased']) / asset['price_purchased']),3)
                asset['current_price'] = current_price[0]
                asset['returns'] = returns
        return True

    def total_returns(self,balance,initial_balance):
        return round(float(((balance + self.value) - initial_balance) / initial_balance),4)
        
    def latest_returns(self,balance):
        value = 0
        for asset in self.portfolio:
            if 'current_price' in asset:
                value += asset['quantity']*asset['current_price']
        return round(float(((balance + value) - self.value) / self.value),4)
       
    def complementary_arrays(self):
        portfolio, market = [],[]
        for date in self.date_master_list:
            portfolio.append({'returns': date['returns']})
            market.append({'returns': date['market_returns']})
        return portfolio,market


    ## Risk Metrics ##
    def alpha(self):
        """
        :returns: float
        """
        beta = self.beta()
        alpha = self.c_portfolio_returns[-1]['returns'] - (self.risk_free[len(self.risk_free)-1].low + beta*(self.c_market_returns[-1]['returns'] - self.risk_free[len(self.risk_free)-1].low))
        return round(alpha,5)
    
    def beta(self):
        """
        :returns: float
        """
        beta = round(float(Calculator.covariance(self.c_portfolio_returns, self.c_market_returns, 'returns') / Calculator.variance(self.c_market_returns, 'returns')),5)
        return beta

    def sharpe(self):
        """
        :returns: float
        """
        portfolio_stdev = Calculator.stdev(self.c_portfolio_returns,'returns')
        sharpe = round(float((self.c_portfolio_returns[-1]['returns'] - self.risk_free[len(self.risk_free)-1].low) / portfolio_stdev),5)
        return sharpe

    def volatility(self):
        """
        :returns: float
        """
        portfolio_stdev = round(Calculator.stdev(self.c_portfolio_returns,'returns'),5)
        return portfolio_stdev


