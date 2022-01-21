from decimal import Decimal
from datetime import date
import os
import requests

#read API and update prices
def get_prices_from_API(theData):
    stocks = ['nvda','ftnt']
    crypto = ['eth','ada']
    #read current usd rate
    usdNOK = currency_API()
    #theData contains a list of Ticker objects in my portfolio
    i = 0
    while i < len(theData):
        ticker = theData[i].get_ticker()
        if ticker in stocks:
            #get todays price from API
            price = stock_API(ticker)
            theData[i].set_currPrice(price*usdNOK)
        elif ticker in crypto:
            #get todays price from API - this price is in NOK!
            price = crypto_API(ticker)
            theData[i].set_currPrice(price)
        
        i += 1
    return theData

#Tcker class
class Ticker():
    def __init__(self, ticker, amount, buyPrice):
        self.ticker = ticker
        self.amount = amount
        self.buyPrice = buyPrice
        self.currPrice = 0.0
    
    def get_ticker(self):
        return self.ticker
    def get_amount(self):
        return self.amount
    def get_buyPrice(self):
        return self.buyPrice
    def get_currPrice(self):
        return self.currPrice
    
    def set_currPrice(self, currPrice):
        self.currPrice = currPrice
        return
    def get_value(self):
        return self.get_amount() * self.get_currPrice()
    def calc_profit(self):
        cost = self.get_amount() * self.get_buyPrice()
        value = self.get_amount() * self.get_currPrice()
        return value-cost
#end class definition

#get current date
def get_todays_date():
    #today = "04.01.2022"
    dateX = date.today()
    #format to dd.mm.YY
    today = dateX.strftime("%d.%m.%Y")
    return today

#convert to decimal from string
def str_to_dec(stringDec):
    stringDec = stringDec.replace(",", ".") 
    decimal = float(stringDec.strip(" '"))
    return decimal

# create the ticker object with all input data included
def get_investment_object(elementTrimmed):
    #three items separated by space-> ticker, amount, buyprice
    splitX = elementTrimmed.split()
    tickerX = splitX[0]
    amountX = splitX[1]
    buyPriceX = splitX[2]
    #convert to decimal from string
    amount = str_to_dec(amountX)
    buyPrice = str_to_dec(buyPriceX)
    #create the ticker object
    tickerObj = Ticker(tickerX, amount, buyPrice)
    return tickerObj

#read portfolio from input file
def get_the_data():
    #read the data from the file 
    theData = open('./app/data/portfolio.txt', 'r')
    #move data into a list - read a line and remove lineshift
    data_list = []
    for element in theData:
        elementTrimmed = element.strip()
        #get a investment object for the data in the row
        ticker = get_investment_object(elementTrimmed)
        #add object to a list
        data_list.append(ticker)
    return data_list

# update the current prices of all the tickers
def addPrices(theData):
    #get current date
    today = get_todays_date()
    #read the norwegian prices from the file
    thePrices = open('./app/data/currprice.txt', 'r')
    stocks = ["nbx"]
    # update the current prices of all the tickers
    for element in thePrices:
        elementTrimmed = element.strip()
        # the data element contain -> ticker, current_price, currency
        splitX = elementTrimmed.split()
        #add currencies to currency objects and date to date string
        if splitX[0] in stocks:
            ticker = splitX[0]
            tickerValue = str_to_dec(splitX[1])
            #update the current price of the ticker in NOK
            i = 0
            while i < len(theData):
                if theData[i].get_ticker() == ticker:
                    theData[i].set_currPrice(tickerValue)
                i += 1
    return today

#loop thru current portfolio and get profit and total value
def get_totals(theData):
    i = 0
    totValue = 0
    totProfit = 0
    portfolioList = []
    while i < len(theData):
        #read profit for the ticker
        ticker = theData[i].get_ticker()
        profit = int(theData[i].calc_profit())
        amount = theData[i].get_amount()
        buyPrice = theData[i].get_buyPrice()
        currPrice = theData[i].get_currPrice()

        #accumulate totals, profit and portfolio
        totProfit += profit
        totValue += int(theData[i].get_value())
        #add ticker data to a dictionary
        tickerData = {
            'ticker': ticker, 
            'profit': profit,
            'buyPrice': buyPrice,
            'currPrice': currPrice,
            'amount': amount
            }        
        portfolioList.append(tickerData)

        #next
        i += 1
    return totValue, totProfit, portfolioList

def start_the_engine():
    #get the portfolio data and read them into a list
    theData = get_the_data()
    #read all the current prices from US from the API
    thePortfolio = get_prices_from_API(theData)

    # add current price to object
    today = addPrices(thePortfolio)

    #calculate total portfolio value and total fortjeneste
    totValue, totProfit, portfolioList = get_totals(thePortfolio)
    #store the data in a new file
    return totValue, totProfit, portfolioList, today

#store portfolio ad current rices in a new file (for Norwegian stocks)
def storePrices(currentTickerData, today):
    newFile = open('./app/data/currprice.txt', 'w')
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

#test if the alpha vantage api works
def stock_API(symbolX):
    xDict = []
    # alpha vantage api syntax
    #url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=NVDA&apikey=ALPHA_KEY'
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
    xDict = []
    #url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=CNY&apikey=demo'
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
    xDict = []
    #url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=CNY&apikey=demo'
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