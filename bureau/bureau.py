
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

@main.route('/delete', methods=['GET', 'POST'])
def delete():
    user = Bureau.query.filter_by(id=8).first()
    if user is not None:
        user.is_blocked = True
        user.save_to_db()
        return redirect(url_for('auth.signup_page'))
    return render_template('/dashboard/edit.html', user=user)

@main.route('/reset-password', methods=('GET', 'POST',))
def forgot_password():
    token = request.args.get('token',None)
    form = EmailForm(request.form) 
    if form.validate_on_submit():
        email = form.email.data
        user = Bureau.query.filter_by(email=email).first()
        if user:
            token = user.get_token()
            print(token)
    return render_template('password_reset_email.html', form=form)

@main.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token,user):
    if token:
        form = PasswordForm(request.form)
        if form.validate_on_submit():
            user.password_hash = generate_password_hash(form.password.data)
            
            user.save_to_db()
            flash("password updated successfully")
            return redirect(url_for('auth.login_page'))
        return render_template('reset_password_with_token.html')
    return render_template('dashboard/edit.html')
    


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