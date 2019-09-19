
from flask import Flask, render_template, request, flash, url_for, redirect, make_response
from .forms import BureauForm, BureauLogin
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .models import * 
from . import app,db
 
@app.route('/registerbureau', methods = ['GET', 'POST'])  
def registerbureau():
    form = BureauForm()
    if form.validate():
        bureau = Bureau(name = form.name.data,
                              address = form.address.data,
                              email = form.email.data,
                              account_no = form.account_no.data,
                              destination_bank = form.destination_bank.data,
                              longitude = form.longitude.data,
                              latitude = form.latitude.data,
                              username = form.username.data,
                              password_hash = generate_password_hash(form.password_hash.data))
                              

        bureau.save_to_db()
        flash('Logged in successfully.')
        return redirect(url_for('login'))
    return render_template('/buyer.html', form=form)

@app.route('/login', methods = ['GET'])
def login():
    form = BureauLogin()
    if form.validate_on_submit():
        bureau = Bureau.get_bureau_by_username(username)
        if bureau is not None and bureau.check_password_hash(form.password_hash.data):
            flash("welcome to the system")
            return redirect(url_for('home'))
        else:
            flash('access denied, make sure you are entering correct credentials')
            return redirect(url_for('login'))
    return redirect(url_for('registerbureau'))
