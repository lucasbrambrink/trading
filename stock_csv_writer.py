## Scraper for all Stock Data for Final Project ##
import csv
import requests


def get_price(symbol):
    base_url = 'https://www.quandl.com/api/v1/datasets/WIKI/'
    auth_token='HdD4E3ee682f2C4mJg11'
    start_day = '2000-01-01'
    end_day = '2014-11-25'
    query_str = base_url + "{}.json?trim_start={}&trim_end{}&auth_token={}".format(symbol, start_day, end_day, auth_token)
    print("Query: ", query_str)
    response = requests.get(query_str, headers={'content-type': 'application/json'})
    a = 0
    while a < 10:
        try:
            r = response.json()
            return r
        except:
            response = requests.get(query_str, headers={'content-type': 'application/json'})
        a += 1  
    return None


'''
    {"urlize_name":"Monsanto-Company-MON-Prices-Dividends-Splits-and-Trading-Volume",
    "data": [
    $"Date","Open","High","Low","Close"$
    ["2014-11-12",118.25,119.487,117.79,118.99, ...]
    ["2014-11-11",116.7,118.36,116.7,118.31,...]
    ]}
'''

def create_the_entire_db():
    stock_list = csv.reader(open('csv_files/stock_list_wiki.csv', newline=''))
    stock_csv = csv.writer(open('stock_prices.csv', 'w', newline=''))
    counter = 0
    for row in stock_list:
        if counter == 0:
            counter += 1
            continue ## first row specifies the collums, needs to be skipped
        prices = get_price(row[0])
        stock_csv.writerow((row[0],row[1],row[2],row[3]))
        for key in prices: ## this is only to avoid a key error if Quandl throws an error, for continuity
            if key == 'data':
                for data_point in prices['data']:
                    ## symbol, date, open, high, low, close
                    stock_csv.writerow((row[0],data_point[0],data_point[1],data_point[2],data_point[3],data_point[4]))
        print("Success : ",row[1])


## Script ##
create_the_entire_db()
print("All is well! Success!")
