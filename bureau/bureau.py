
from flask import Flask, render_template, request, flash, url_for, redirect, make_response
from .forms import SignupForm, LoginForm, EmailForm, PasswordForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
#from flask.ext.login import current_user, login_required, login_user, logout_user, redirect, url_for
from .models import * 
from . import app,db
from flask import Blueprint
from flask_login import current_user
from flask import current_app as app
from flask_login import login_required
from .token import generate_confirmation_token, confirm_token
from itsdangerous import URLSafeTimedSerializer
from flask_login import login_required, logout_user, current_user, login_user
from .import login_manager
import datetime
from bureau.email import send_email



# Blueprint Configuration
main = Blueprint('main', __name__,
                    template_folder='templates',
                    static_folder='static')


@main.route('/block', methods=['GET', 'POST'])
@login_required
def block():
    user = Bureau.query.filter_by(id=current_user.id).first()
    if user is not None:
        user.is_blocked = True
        user.save_to_db()
        return redirect(url_for('auth.login_page'))
    return render_template('/dashboard/edit.html', user=user)


@main.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = Bureau.query.filter_by(email=form.email.data).first()         
        if user:
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('main.confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
           
        else:
            flash('Your email address must be confirmed before attempting a password reset.', 'error')
            return redirect(url_for('auth.login_page'))
 
    return render_template('password_reset_email.html', form=form)

@main.route('/confirm/<token>', methods = ['GET', 'POST'])
#@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = Bureau.query.filter_by(email=email).first_or_404()
    if user:
        form = PasswordForm()
 
        if form.validate_on_submit():
            try:
                user = Bureau.query.filter_by(email=email).first_or_404()
            except:
                flash('Invalid email address!', 'error')
                return redirect(url_for('auth.login_page'))

            user.password_hash = form.password.data
            user.save_to_db()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('auth.login_page'))

        return render_template('reset_password_with_token.html', form=form, token=token)
 
            
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