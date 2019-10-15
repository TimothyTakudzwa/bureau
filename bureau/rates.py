
from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import RatesForm
from .models import *
from . import app,db

@app.route('/rates', methods=['GET', 'POST'])
def rates():
    form = RatesForm()
    print(form.validate())
    if request.method == 'POST':
      print("=========~~~~~~~~~~~~~~~~~~~~~~~~~============")
      rate = Rates  ( rate = form.rate.data,
                        client_id = form.name.data,
                        currency_a = form.currency_a.data,
                        currency_b = form.currency_b.data
                        )
      rate.save_to_db()
      flash('Rate uploaded!!!', 'success')
    return render_template('dashboard/add_rate.html', form = form)
