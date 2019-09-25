from flask import Flask, render_template, request, flash, url_for, session,redirect
from functools import wraps
from .models import *
from . import app,db
from .forms import RatesForm

@app.route('/ratesview', methods=['GET', 'POST'])
def ratesview():
    today = datetime.now()
    session_id = 2
    bureau_rates = Rates.query.filter_by(bureau_id=session_id)
    rates_today = Rates.query.filter_by(date=today)

    form = RatesForm()
    print(form.validate())
    if request.method == 'POST':
      print("=========~~~~~~~~~~~~~~~~~~~~~~~~~============")
      rate = Rates  ( rate = form.rate.data,
                        bureau_id = 2,
                        currency_a = form.currency_a.data,
                        currency_b = form.currency_b.data,
                        action = form.action.data
                        )
      rate.save_to_db()
      flash('Rate uploaded!!!', 'success')
      return redirect(url_for('ratesview'))
    return render_template('dashboard/ratesview.html', rates_today=rates_today, bureau_rates=bureau_rates, form=form)


@app.route('/rates_today', methods=['GET', 'POST'])
def rates_today():
    today = datetime.now()
    rates_today = Rates.query.filter_by(date=today)
    return render_template('dashboard/rates_today.html', rates_today=rates_today)