"""
This file contains all the logic to ear data and calulate the
portfolio value
"""

from decimal import Decimal
from datetime import date
import os
import requests

def get_prices_from_api(ticker_data):
    """
    Read the Alpha Vantage API to get current prices
    for currency, stock & crypto in portfolio
    """
    stocks = ['nvda','ftnt']
    crypto = ['eth','ada']
    #read current usd rate
    usd_nok = currency_API()
    #ticker_data contains a list of Ticker objects in my portfolio
    i = 0
    while i < len(ticker_data):
        ticker = ticker_data[i].get_ticker()
        if ticker in stocks:
            #get todays price from API
            price = stock_API(ticker)
            ticker_data[i].set_curr_price(price*usd_nok)
        elif ticker in crypto:
            #get todays price from API - this price is in NOK!
            price = crypto_API(ticker)
            ticker_data[i].set_curr_price(price)
        i += 1
    return ticker_data

class Ticker():
    """
    create objects for all tickers in portfolio. this is used to
    get / set all relevant info on a ticker; incl current price.
    """
    def __init__(self, ticker, amount, buy_price):
        self.ticker = ticker
        self.amount = amount
        self.buy_price = buy_price
        self.curr_price = 0.0
    def get_ticker(self):
        """
        get ticker symbol of object
        """
        return self.ticker
    def get_amount(self):
        """
        get the number of shares of object we have in portfolio
        """
        return self.amount
    def get_buy_price(self):
        """
        get the buy price for the investment object (ticker)
        """
        return self.buy_price
    def get_curr_price(self):
        """
        get the current price for the investment object (ticker)
        """
        return self.curr_price
    def set_curr_price(self, curr_price):
        """
        set the current price for the investment object (ticker)
        """
        self.curr_price = curr_price

    def get_value(self):
        """
        calculate the current value for the investment object (ticker)
        """
        return self.get_amount() * self.get_curr_price()
    def calc_profit(self):
        """
        calculate the current value for the overall portfolio
        """
        cost = self.get_amount() * self.get_buy_price()
        value = self.get_amount() * self.get_curr_price()
        return value-cost

def get_todays_date():
    """
    fetch todays date
    """
    curr_date = date.today()
    #format to dd.mm.YY
    today = curr_date.strftime("%d.%m.%Y")
    return today

def str_to_dec(string_dec):
    """
    convert to decimal from string
    """
    string_dec = string_dec.replace(",", ".")
    decimal = float(string_dec.strip(" '"))
    return decimal

def get_investment_object(ticker_element):
    """
    create the ticker object with all input data included
    three items separated by space-> ticker, amount, buy_price
    """
    ticker_item_list = ticker_element.split()
    ticker = ticker_item_list[0]
    amount = ticker_item_list[1]
    buy_price = ticker_item_list[2]
    #convert to decimal from string
    amount = str_to_dec(amount)
    buy_price = str_to_dec(buy_price)
    #create the ticker object
    ticker_obj = Ticker(ticker, amount, buy_price)
    return ticker_obj

def get_the_data():
    """
    read portfolio from input file
    """
    ticker_data = open('./app/data/portfolio.txt', 'r')
    #move data into a list - read a line and remove lineshift
    data_list = []
    for element in ticker_data:
        ticker_element = element.strip()
        #get a investment object for the data in the row
        ticker = get_investment_object(ticker_element)
        #add object to a list
        data_list.append(ticker)
    return data_list

def addPrices(ticker_data):
    """
    update the current prices of all the tickers
    """
    today = get_todays_date()
    #read the norwegian prices from the file
    thePrices = open('./app/data/curr_price.txt', 'r')
    stocks = ["nbx"]
    # update the current prices of all the tickers
    for element in thePrices:
        ticker_element = element.strip()
        # the data element contain -> ticker, current_price, currency
        ticker_item_list = ticker_element.split()
        #add currencies to currency objects and date to date string
        if ticker_item_list[0] in stocks:
            ticker = ticker_item_list[0]
            tickerValue = str_to_dec(ticker_item_list[1])
            #update the current price of the ticker in NOK
            i = 0
            while i < len(ticker_data):
                if ticker_data[i].get_ticker() == ticker:
                    ticker_data[i].set_curr_price(tickerValue)
                i += 1
    return today

def get_totals(ticker_data):
    """
    loop thru current portfolio and get profit and total value
    """
    i = 0
    totValue = 0
    totProfit = 0
    portfolioList = []
    while i < len(ticker_data):
        #read profit for the ticker
        ticker = ticker_data[i].get_ticker()
        profit = int(ticker_data[i].calc_profit())
        amount = ticker_data[i].get_amount()
        buy_price = ticker_data[i].get_buy_price()
        curr_price = ticker_data[i].get_curr_price()
        #accumulate totals, profit and portfolio
        totProfit += profit
        totValue += int(ticker_data[i].get_value())
        #add ticker data to a dictionary
        tickerData = {
            'ticker': ticker,
            'profit': profit,
            'buy_price': buy_price,
            'curr_price': curr_price,
            'amount': amount
            }
        portfolioList.append(tickerData)
        #next
        i += 1
    return totValue, totProfit, portfolioList

def start_the_engine():
    """
    get the portfolio data and read them into a list
    """
    #get the portfolio data and read them into a list
    ticker_data = get_the_data()
    #read all the current prices from US from the API
    thePortfolio = get_prices_from_api(ticker_data)
    # add current price to object
    today = addPrices(thePortfolio)
    #calculate total portfolio value and total fortjeneste
    totValue, totProfit, portfolioList = get_totals(thePortfolio)
    #store the data in a new file
    return totValue, totProfit, portfolioList, today

def storePrices(currentTickerData, today):
    """
    store portfolio ad current rices in a new file (for Norwegian stocks)
    """
    newFile = open('./app/data/curr_price.txt', 'w')
    #loop thru all objects and add to txt file
    i = 0
    rows = []
    #first row is the current date
    rows.append("date "+today+"\n")
    #then add remaining rows from user input
    while i < len(currentTickerData):
        rows.append(currentTickerData[i] + "\n")
        i += 1
    newFile.writelines(rows)
    newFile.close()
    return

def stock_API(symbolX):
    """
    read the Aplha Vantage API. alpha vantage api syntax
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=NVDA&apikey=ALPHA_KEY'
    """
    xDict = []
    tickerX = 'symbol=' + symbolX
    apiX = '&apikey='+'9PN7WYC36TLO0Z09'
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&'+ tickerX + apiX
    r = requests.get(url)
    # the data received from the API
    apiData = r.json()
    #fecth the global quote
    xDict = apiData.get('Global Quote')
    #check if we have overloaded the API - only 5 calls pr minute
    if xDict == None:
        #API is overloaded
        priceX = 0.0
    else:
        # the closing price is in element 05. price
        price = xDict['05. price']
        priceX = float(price.strip(" '"))
    return priceX

def currency_API():
    """
    read the Aplha Vantage API.
    """
    xDict = []
    apiX = '&apikey='+'9PN7WYC36TLO0Z09'
    currX = '&from_currency=USD&to_currency=NOK'
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE'+currX+apiX
    r = requests.get(url)
    # the data received from the API
    apiData = r.json()
    #fecth the global quote
    xDict = apiData.get('Realtime Currency Exchange Rate')
    #check if we have overloaded the API - only 5 calls pr minute
    if xDict == None:
        #API is overloaded
        priceX = 0.0
    else:
        # the closing price is in element 5
        price = xDict['5. Exchange Rate']
        priceX = float(price.strip(" '"))
    return priceX

def crypto_API(symbolX):
    """
    read the Aplha Vantage API.
    """
    xDict = []
    apiX = '&apikey='+'9PN7WYC36TLO0Z09'
    currX = '&from_currency='+symbolX+'&to_currency=NOK'
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE'+currX+apiX
    r = requests.get(url)
    # the data received from the API
    apiData = r.json()
    #fecth the global quote
    xDict = apiData.get('Realtime Currency Exchange Rate')
    #check if we have overloaded the API - only 5 calls pr minute
    if xDict == None:
        #API is overloaded
        priceX = 0.0
    else:
        # the closing price is in element 5
        price = xDict['5. Exchange Rate']
        priceX = float(price.strip(" '"))
    return priceX
