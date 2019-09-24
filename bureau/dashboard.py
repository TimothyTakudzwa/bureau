
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


def offer_exists(request_id,offer_id):
    offer = Offer.query.filter_by(id=offer_id)
    offer = offer.filter_by(request_id=request_id).first()
    return offer    

@app.route('/requests', methods=['GET', 'POST'])
def requests():
    my_requests = Requests.query.all()

    for my_request in my_requests:
        offer = Offer.query.filter(Offer.request_id == my_request.id).filter(Offer.client_id == 1).first()
        if offer is not None: 
            my_request.my_offer = f"{offer.amount}@{offer.rate}"
        else:
            my_request.my_offer = 0

    
    form = OfferForm()
    if request.method == 'POST' and form.validate():
        offer = Offer( request_id = form.request_id.data,
                       client_id = form.client_id.data,
                       amount = form.offer_amount.data,
                       date = form.date.data,
                       rate = form.rate.data, )
        offer.save_to_db()
        flash('Offer Posted Successfully')               
    return render_template('dashboard/requests.html', requests=my_requests
    , form=form)

'''
@app.route('compare/<bureau_a>', methods=['GET'])
def compare(bureau_a):
    page = request.args.get('page', default = 1, type = int)
    return bureau_a

'''


