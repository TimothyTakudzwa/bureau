# Load data preprocessing libraries
import pandas as pd
import numpy as np
# Load vectorizer and similarity measure
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, flash, url_for, session
from functools import wraps
from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ClientForm, OfferForm
from .models import *
from . import app,db
from flask_login import login_required, logout_user, current_user, login_user
from .import login_manager
from twilio.twiml.messaging_response import MessagingResponse

from datetime import datetime, timedelta 

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard_index():
    rates = Rates.query.all()
    return render_template('dashboard/index.html', rates=rates)

@app.route('/', methods=['GET'])
def landing_index():
    return render_template('landing/index.html')


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
                       client_id = 1,
                       amount = form.offer_amount.data,
                       date = datetime.now(),
                       rate = form.rate.data, )
        try:
            offer.save_to_db()
            flash('Offer Posted Successfully')
            return redirect(url_for('requests'))  
        except:
            flash(f"Failed To Save")
            return redirect(url_for('requests'))            
                     
    return render_template('dashboard/requests.html', requests=my_requests
    , form=form)

@app.route('/profile', methods=['GET','POST'])
@login_required
def user_profile():
    user = Bureau.query.filter_by(id = current_user.id).first()
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.address = request.form.get('address')
        user.email = request.form.get('email')
        user.account_no = request.form.get('account_no')
        user.destination_bank = request.form.get('destination_bank')
        user.username = request.form.get('username')
        user.phone = request.form.get('phone')
       
        user.save_to_db()
        flash('your  changes were saved.')
        return redirect(url_for('user_profile'))
    return render_template('dashboard/edit.html', user=user)

@app.route('/trading', methods=['GET', 'POST'])
def trading():
    df = pd.read_csv("my_csv.csv")
    df.columns = ["Sentence","Category"]
    df.dropna(inplace=True)
    # Train the vectorizer
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate((df.Sentence, df.Category)))
    # Vectorize sentences
    Sentence_vectors = vectorizer.transform(df.Sentence)
    
    # user input
    input_sentence = request.form.get('input_sentence')
    # Locate the closest sentence
    input_sentence_vector = vectorizer.transform([input_sentence])

    # Compute similarities
    similarities = cosine_similarity(input_sentence_vector, Sentence_vectors)

    # Find the closest question
    closest = np.argmax(similarities, axis=1)
    category = df.Category.iloc[closest].values[0]
    
        
    return render_template('trading.html', category = category, input_sentence = input_sentence)


@app.route('/prof', methods=['GET'])
def prof():
    user = Bureau.query.filter_by(id=4).all()
    return render_template('dashboard/user.html', user=user)

@app.route('/compare/<bureau_a>', methods=['GET'])
def compare(bureau_a):
    page = request.args.get('page', default = 1, type = int)
    return bureau_a

@app.route('/edit_')
def method_name():
   pass


@app.route('/my-route')
def my_route():
  page = request.args.get('page', default = 1, type = int)
  page = Bureau.query.filter(id == page).first()
  filter = request.args.get('filter', default = '*', type = str)
  print(page)
  print(filter)
  return f"{page}Success"

