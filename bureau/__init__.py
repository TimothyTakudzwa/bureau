from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_object('config')

from . import views, models, app, db, bureau, client, rates, dashboard
