from app import app
from flask import render_template, redirect, url_for
from app.forms import InputForm
from app.models import *

#the ticker, their current value and currency
currTickerData = []
portf_list = []

@app.route('/')
@app.route('/home')
def home():
    posts = "lets get this party started!"
    return render_template('home.html', title='Home', posts=posts)

@app.route('/manual', methods=['GET', 'POST'])
def manual():
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
    #read current portfolio based on current prices
    tot_value, tot_profit, portf_list, today = start_the_engine()
    return render_template('output.html', title='Portefølje', posts=portf_list, value = tot_value, profit = tot_profit, today=today)
