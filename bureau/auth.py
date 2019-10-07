
"""Routes for user authentication."""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from .forms import LoginForm, SignupForm
from .models import db, Bureau
from .import login_manager


# Blueprint Configuration
auth = Blueprint('auth', __name__,
                    template_folder='templates',
                    static_folder='static')


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    """User login page."""
    #if current_user.is_authenticated:
        #return redirect(url_for('main.dashboard'))
    form = LoginForm()
    print(form.validate())
    if request.method == 'POST':
       
        username = form.username.data
        password = form.password.data
        user = Bureau.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                if user.is_blocked==False:
                    login_user(user)
                    return redirect(url_for('dashboard_index'))
                flash('your account is blocked')
                return redirect(url_for('auth.login_page'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth.login_page'))
    
           
    return render_template('login.html',
                           form=form,
                           template='login-page',
                           body="Log in with your User account.")


@auth.route('/signup', methods=['GET', 'POST'])
def signup_page():
    form = SignupForm()
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
        return redirect(url_for('auth.login_page'))
    return render_template('/signup.html',
                           title='Create an Account',
                           form=SignupForm(),
                           template='signup-page',
                           body="Sign up for a user account.")
@auth.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('auth.login_page'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return Bureau.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login_page'))'''
