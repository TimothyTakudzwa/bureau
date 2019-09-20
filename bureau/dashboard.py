from flask import Flask, render_template, request, flash, url_for. session
from functools import wraps
from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ClientForm
from .models import *
from . import app,db

from datetime import datetime, timedelta

@app.route('/dashboard', methods=['GET'])
def dashboard_index():
    rates = Rates.query.all()
    return render_template('dashboard/index.html', rates=rates)

@app.route('/exchange_rates', methods=['GET'])
def exchange_rate():
    today = datetime.now()
    rates = Rates.query.all()
    rates_today = Rates.query.filter_by(date=today)
    '''
    last_week = datetime.datetime.now() - timedelta(days=7)
    
    '''
    return render_template('dashboard/exchange_rate.html',
     rates=rates, rates_today=rates_today)

 