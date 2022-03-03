"""
This file contains all the logic to read the data and calculate the
portfolio value
"""

from datetime import date
import requests

def get_prices_from_api(ticker_data):
    """
    Read the Alpha Vantage API to get current prices
    for currency, stock & crypto in portfolio
    """
    stocks = ['nvda','ftnt']
    crypto = ['eth','ada']
    #read current usd rate
    usd_nok = currency_api()
    #ticker_data contains a list of Ticker objects in my portfolio
    i = 0
    while i < len(ticker_data):
        ticker = ticker_data[i].get_ticker()
        if ticker in stocks:
            #get todays price from API
            price = stock_api(ticker)
            ticker_data[i].set_curr_price(price*usd_nok)
        elif ticker in crypto:
            #get todays price from API - this price is in NOK!
            price = crypto_api(ticker)
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
    ticker_data = open('./app/data/portfolio.txt', 'r', encoding='utf-8')
    #move data into a list - read a line and remove lineshift
    data_list = []
    for element in ticker_data:
        ticker_element = element.strip()
        #get a investment object for the data in the row
        ticker = get_investment_object(ticker_element)
        #add object to a list
        data_list.append(ticker)
    return data_list

def add_prices(ticker_data):
    """
    update the current prices of all the tickers
    """
    today = get_todays_date()
    #read the norwegian prices from the file
    the_prices = open('./app/data/curr_price.txt', 'r', encoding='utf-8')
    stocks = ["nbx", "skagen"]
    # update the current prices of all the tickers
    for element in the_prices:
        ticker_element = element.strip()
        # the data element contain -> ticker, current_price, currency
        ticker_item_list = ticker_element.split()
        #add currencies to currency objects and date to date string
        if ticker_item_list[0] in stocks:
            ticker = ticker_item_list[0]
            ticker_value = str_to_dec(ticker_item_list[1])
            #update the current price of the ticker in NOK
            i = 0
            while i < len(ticker_data):
                if ticker_data[i].get_ticker() == ticker:
                    ticker_data[i].set_curr_price(ticker_value)
                i += 1
    return today

def get_totals(ticker_data):
    """
    loop thru current portfolio and get profit and total value
    """
    i = 0
    tot_value = 0
    tot_profit = 0
    portf_list = []
    while i < len(ticker_data):
        #read profit for the ticker
        ticker = ticker_data[i].get_ticker()
        profit = int(ticker_data[i].calc_profit())
        amount = ticker_data[i].get_amount()
        buy_price = ticker_data[i].get_buy_price()
        curr_price = ticker_data[i].get_curr_price()
        #accumulate totals, profit and portfolio
        tot_profit += profit
        tot_value += int(ticker_data[i].get_value())
        #add ticker data to a dictionary
        ticker_info = {
            'ticker': ticker,
            'profit': profit,
            'buy_price': buy_price,
            'curr_price': curr_price,
            'amount': amount
            }
        portf_list.append(ticker_info)
        #next
        i += 1
    return tot_value, tot_profit, portf_list

def start_the_engine():
    """
    get the portfolio data and read them into a list
    """
    #get the portfolio data and read them into a list
    ticker_data = get_the_data()
    #read all the current prices from US from the API
    the_portf = get_prices_from_api(ticker_data)
    # add current price to object
    today = add_prices(the_portf)
    #calculate total portfolio value and total fortjeneste
    tot_value, tot_profit, portf_list = get_totals(the_portf)
    #store the data in a new file
    return tot_value, tot_profit, portf_list, today

def store_prices(curr_ticker_list, today):
    """
    store portfolio ad current rices in a new file (for Norwegian stocks)
    """
    new_file = open('./app/data/curr_price.txt', 'w', encoding='utf-8')
    #loop thru all objects and add to txt file
    i = 0
    rows = []
    #first row is the current date
    rows.append("date "+today+"\n")
    #then add remaining rows from user input
    while i < len(curr_ticker_list):
        rows.append(curr_ticker_list[i] + "\n")
        i += 1
    new_file.writelines(rows)
    new_file.close()

def stock_api(symbol):
    """
    read the Aplha Vantage API. alpha vantage api syntax
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=NVDA&apikey=ALPHA_KEY'
    """
    api_dict = []
    ticker = 'symbol=' + symbol
    api_key = '&apikey='+'9PN7WYC36TLO0Z09'
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&'+ ticker + api_key
    conn = requests.get(url)
    # the data received from the API
    api_data = conn.json()
    #fecth the global quote
    api_dict = api_data.get('Global Quote')
    #check if we have overloaded the API - only 5 calls pr minute
    if api_dict is None:
        #API is overloaded
        curr_price = 0.0
    else:
        # the closing price is in element 05. price
        price = api_dict['05. price']
        curr_price = float(price.strip(" '"))
    return curr_price

def currency_api():
    """
    read the Aplha Vantage API.
    """
    api_dict = []
    api_key = '&apikey='+'9PN7WYC36TLO0Z09'
    currency = '&from_currency=USD&to_currency=NOK'
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE'+currency+api_key
    conn = requests.get(url)
    # the data received from the API
    api_data = conn.json()
    #fecth the global quote
    api_dict = api_data.get('Realtime Currency Exchange Rate')
    #check if we have overloaded the API - only 5 calls pr minute
    if api_dict is None:
        #API is overloaded
        curr_price = 0.0
    else:
        # the closing price is in element 5
        price = api_dict['5. Exchange Rate']
        curr_price = float(price.strip(" '"))
    return curr_price

def crypto_api(symbol):
    """
    read the Aplha Vantage API.
    """
    api_dict = []
    api_key = '&apikey='+'9PN7WYC36TLO0Z09'
    currency = '&from_currency='+symbol+'&to_currency=NOK'
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE'+currency+api_key
    conn = requests.get(url)
    # the data received from the API
    api_data = conn.json()
    #fecth the global quote
    api_dict = api_data.get('Realtime Currency Exchange Rate')
    #check if we have overloaded the API - only 5 calls pr minute
    if api_dict is None:
        #API is overloaded
        curr_price = 0.0
    else:
        # the closing price is in element 5
        price = api_dict['5. Exchange Rate']
        curr_price = float(price.strip(" '"))
    return curr_price
