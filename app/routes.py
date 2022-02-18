"""

This Flask app has my portfolio of stocks & crypto in a text file
It uses the Aplha Vantage API to read the current values and the usd -> nok
currency value. my Aplha Vantage key is listed in the .env file
    alpha vantage api syntax
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=NVDA&apikey=ALPHA_KEY'
The applicaton is hosted at Heroku

 --
(virtu) geirowe@geirs-imac portfolio % python3 -m pylint ./app/routes.py
Your code has been rated at 10.00/10 

"""

from flask import render_template, redirect, url_for
from app import app
from app.forms import InputForm
from app.models import storePrices, get_todays_date, start_the_engine

#the ticker, their current value and currency
currTickerData = []

@app.route('/')
@app.route('/home')
def home():
    """
    This is the home page of my app
    """
    posts = "lets get this party started!"
    return render_template('home.html', title='Home', posts=posts)

@app.route('/manual', methods=['GET', 'POST'])
def manual():
    """
    This is the form to add ticker values that can not be
    read from the Alpha Vantage API. Typically this applies
    for non-US companies
    """
    form = InputForm()
    if form.validate_on_submit():
        #sjekk hvilken submit buttion som er trykket
        if form.send.data:
            #lagre data og avslutt
            currTickerData.append(form.ticker.data+" "+form.currValue.data+" "+form.currency.data)
            #get current date
            today = get_todays_date()
            #store the current prices in a file
            storePrices(currTickerData, today)
            return redirect(url_for('home'))
        if form.oneMore.data:
            #lagre data og fortsett med å lese inn data
            currTickerData.append(form.ticker.data+" "+form.currValue.data+" "+form.currency.data)
            return redirect(url_for('manual'))
    return render_template('manual.html', title='Input', form=form)

@app.route('/output')
def output():
    """
    This is the form to display my total portfolio listings and value
    """
    #read current portfolio based on current prices
    portf_list = []
    tot_value, tot_profit, portf_list, today = start_the_engine()
    return render_template('output.html', title='Portefølje', posts=portf_list, \
        value = tot_value, profit = tot_profit, today=today)
