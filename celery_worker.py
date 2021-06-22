""" configure celery worker instance """
from app import app, celery_app
from app.celery_utils import init_celery

app.app_context().push()

init_celery(celery_app, app)
