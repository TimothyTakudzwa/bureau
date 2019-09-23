from flask import Flask, render_template, request, flash, url_for, redirect, make_response
from .forms import BureauForm, BureauLogin
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
#from flask.ext.login import current_user, login_required, login_user, logout_user, redirect, url_for
from .models import * 
from . import app,db
 
@app.route('/registerbureau', methods = ['GET', 'POST'])  
def registerbureau():
    form = BureauForm()
    if form.validate_on_submit():
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
        flash('you can login now')
        return redirect(url_for('login'))
    return render_template('/registration.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = BureauLogin(request.form)
    if form.validate_on_submit():
        bureau = Bureau.query.filter_by(username=form.username.data).first()
        if bureau is not None and bureau.verify_password(form.password_hash.data):
            return redirect(url_for('dashboard'))
    flash("failed to login")        
    return render_template('/login.html', form=form)
    

@app.route('/landing')
def landing():
    return render_template('landing/index.html')

@app.route('/log')
def log():
    return render_template('/landing/login.html')

@app.route('/about')
def about():
    return render_template('/landing/about.html')

@app.route('/services')
def services():
    return render_template('/landing/services.html')

#@app.route('/register')
#def register():
    #return render_template('/landing/register.html')