
from flask import Flask, render_template, request, flash, url_for, session
from functools import wraps
from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ClientForm, OfferForm
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
    form = OfferForm(request.form)
    rates_today = Rates.query.filter_by(date=today)

    return render_template('dashboard/exchange_rate.html',
     rates=rates, rates_today=rates_today, form=form)

@app.route('/requests', methods=['GET'])
def requests():
    requests = Requests.query.all()
    form = OfferForm(request.form)
    return render_template('dashboard/requests.html', requests=requests
    , form=form)

@app.route('/profile', methods=['GET','POST'])
def user_profile():

    user = Bureau.query.filter_by(id=1).first()
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.address = request.form.get('address')
        user.email = request.form.get('email')
        user.account_no = request.form.get('account_no')
        user.destination_bank = request.form.get('destination_bank')
        user.username = request.form.get('username')
       
        user.save_to_db()
        flash('your  changes were saved.')
        return redirect(url_for('user_profile'))
    return render_template('dashboard/edit.html', user=user)

'''
@app.route('/prof', methods=['GET'])
def prof():
    user = Bureau.query.filter_by(id=4).all()
    return render_template('dashboard/user.html', user=user)

@app.route('compare/<bureau_a>', methods=['GET'])
def compare(bureau_a):
    page = request.args.get('page', default = 1, type = int)
    return bureau_a

'''

