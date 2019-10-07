
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
import os
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_object('config')


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'intelliwhatsappbanking@gmail.com'
app.config['MAIL_PASSWORD'] = 'intelli12345#'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


login_manager = LoginManager()
login_manager.session_protection = 'strong'
#login_manager.login_view = 'main.login'
db.init_app(app)
login_manager.init_app(app)

with app.app_context():
        # Import parts of our application
        from . import bureau
        from . import auth

        # Register Blueprints
        app.register_blueprint(bureau.main)
        app.register_blueprint(auth.auth)

from . import views, models, app, db, bureau, client, rates, dashboard, bureau_rates
from . import views, models, app, db, bureau, client, rates, dashboard, mytransactions, response
