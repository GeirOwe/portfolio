from decimal import Decimal
from datetime import date

#Currency class
class Currency():
    def __init__(self, curr, price):
        self.curr = curr
        self.price = price
    def get_price(self):
        return self.price    
    
    def get_curr(self):
        return self.curr
#end currency class

#Tcker class
class Ticker():
    def __init__(self, ticker, amount, buyPrice):
        self.ticker = ticker
        self.amount = amount
        self.buyPrice = buyPrice
    
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

#find current listing for the currency
def get_currency(currency, valutaList):
    #loop thru all currencies and get the price
    value = 1.0
    i = 0
    while i < len(valutaList):
        if valutaList[i].get_curr() == currency:
            value = valutaList[i].get_price()
        i += 1
    return value

#convert to decimal from string
def str_to_dec(stringDec):
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
     #read the prices from the file
    thePrices = open('./app/data/currprice.txt', 'r')
    valuta = ["usd", "nok", "date"]
    valutaList = []
    # update the current prices of all the tickers
    for element in thePrices:
        elementTrimmed = element.strip()
        # the data element contain -> ticker, current_price, currency
        splitX = elementTrimmed.split()
        #add currencies to currency objects and date to date string
        if splitX[0] in valuta:
            if splitX[0] == "date":
                today = splitX[1]
            else:
                currencyValue = str_to_dec(splitX[1])   #convert from string to dec
                currency = Currency(splitX[0], currencyValue)
                valutaList.append(currency)
        else:
            #split the data -> ticker, tickerValue, currency
            ticker = splitX[0]
            tickerValue = str_to_dec(splitX[1])
            currency = splitX[2]
            # get the current listing for the curency
            currencyValue = get_currency(currency, valutaList)
            #update the current price of the ticker
            i = 0
            while i < len(theData):
                if theData[i].get_ticker() == ticker:
                    theData[i].set_currPrice(tickerValue*currencyValue)
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
    #get the data and read them into a list
    theData = get_the_data()
    #read all the current prices for the tickers from user
    # add current price to object
    today = addPrices(theData)

    #calculate total portfolio value and total fortjeneste
    totValue, totProfit, portfolioList = get_totals(theData)
    #store the data in a new file
    return totValue, totProfit, portfolioList, today

#store portfolio ad current rices in a new file
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