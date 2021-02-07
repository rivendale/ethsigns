from config import AppConfig
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restplus import apidoc
from flask_sqlalchemy import SQLAlchemy
from app.api import signs_ns

from app.api import api_blueprint
from app.api.resources import api

authorizations = {'Bearer Auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
}}


signs_path = "signs/"
api.add_namespace(signs_ns, path=signs_path)


"""Return app object given config object."""
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(AppConfig)
Bootstrap(app)
db = SQLAlchemy(app)
api.init_app(app)
migrate = Migrate()
migrate.init_app(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = 'login'


@app.route('/api/v1/doc/', endpoint='doc')
def swagger_ui():
    return apidoc.ui_for(api)


app.register_blueprint(api_blueprint)

from app.api import views
from app import routes