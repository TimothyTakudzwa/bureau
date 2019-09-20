from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask.ext.login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_object('config')

#login_manager = LoginManager()
#login_manager.session_protection = 'strong'
#login_manager.login_view = 'main.login'



#db.init_app(app)
#login_manager.init_app(app)


from . import views, models, app, db, bureau, client, rates, dashboard
