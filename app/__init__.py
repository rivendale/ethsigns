from celery import Celery
from config import AppConfig
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restplus import apidoc
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_caching import Cache
from celery.utils.log import get_task_logger
from contextlib import contextmanager

from app.api import api_blueprint, signs_ns
from app.api.resources import api


logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


authorizations = {'Bearer Auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
}}


signs_path = "signs/"
api.add_namespace(signs_ns, path=signs_path)


celery_app = Celery(__name__, broker=AppConfig.REDIS_URL)

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': AppConfig.REDIS_URL
})

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(AppConfig)
celery_app.conf.update(app.config)
cache.init_app(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
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

from app import routes
from app.api import views
from app.api.contract import contract_actions
