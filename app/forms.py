from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired()])
    currentValue = StringField('Value', validators=[DataRequired()])
    currency = StringField('Valuta', default="usd")
    send = SubmitField('Ferdig')
    oneMore = SubmitField('Fortsett')

#class OutputForm(FlaskForm):
#    value = StringField('Portefølje verdi')
#    profit = StringField('Fortjeneste')
    # legg til: ticker, andeler, pålydende, nåværende verdi, fortjeneste
