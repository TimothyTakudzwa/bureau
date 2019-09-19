
from flask import Flask, render_template, request, flash, url_for
from functools import wraps
from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ClientForm
from .models import *
from . import app,db


@app.route('/dashboard', methods=['GET'])
def dashboard_index():
    rates = Rates.query.all()
    return render_template('dashboard/index.html', rates=rates)

@app.route('/exchange_rates', methods=['GET'])
def exchange_rate():
    rates = Rates.query.all()
    return render_template('dashboard/exchange_rate.html')

