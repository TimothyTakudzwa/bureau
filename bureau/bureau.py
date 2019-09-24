
from flask import Flask, render_template, request, flash, url_for, redirect, make_response
from .forms import SignupForm, LoginForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
#from flask.ext.login import current_user, login_required, login_user, logout_user, redirect, url_for
from .models import * 
from . import app,db
from flask import Blueprint
from flask_login import current_user
from flask import current_app as app
from flask_login import login_required

# Blueprint Configuration
main = Blueprint('main', __name__,
                    template_folder='templates',
                    static_folder='static')



@main.route('/', methods=['GET'])
@login_required
def dashboard():
   return render_template('profile.html',
                           template='dashboard-template',
                           current_user=current_user,
                           body="You are now logged in!")

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