from app import app
from flask import render_template, redirect, url_for
from app.forms import InputForm
from app.models import *


#the ticker, their current value and currency
currentTickerData = []
portfolioList = []

@app.route('/')
@app.route('/home')
def home():
    posts = "lets get this party started!"
    return render_template('home.html', title='Home', posts=posts)

@app.route('/input', methods=['GET', 'POST'])
def input():
    form = InputForm()
    if form.validate_on_submit():
        #sjekk hvilken submit buttion som er trykket
        if form.send.data:
            #lagre data og avslutt
            currentTickerData.append(form.ticker.data+" "+form.currentValue.data+" "+form.currency.data)
            #get current date
            today = get_todays_date()
            #store the current prices in a file
            storePrices(currentTickerData, today)
            return redirect(url_for('home'))
        if form.oneMore.data:
            #lagre data og fortsett med å lese inn data
            currentTickerData.append(form.ticker.data+" "+form.currentValue.data+" "+form.currency.data)
            return redirect(url_for('input'))   
    return render_template('input.html', title='Input', form=form)

@app.route('/output')
def output():
    #read current portfolio based on current prices
    totValue, totProfit, portfolioList, today = start_the_engine()
    return render_template('output.html', title='Portefølje', posts=portfolioList, value = totValue, profit = totProfit, today=today)