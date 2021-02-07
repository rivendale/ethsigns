from config import AppConfig
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from app.api.resources import api

authorizations = {'Bearer Auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
}}




"""Return app object given config object."""
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(AppConfig)
Bootstrap(app)
db = SQLAlchemy(app)
api.init_app(app)
Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


from app.api import views
from app import routes

