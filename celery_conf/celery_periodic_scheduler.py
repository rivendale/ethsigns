"""Configuring Celery Beat used for running periodic tasks"""

# Third Party
from datetime import timedelta

# Services
from app import celery_app

celery_app.conf.beat_schedule = {


    'complete-pending-transactions': {
        'task': 'complete-pending-transactions',
        'schedule': timedelta(seconds=10),
    },
}
