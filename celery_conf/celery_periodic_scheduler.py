"""Configuring Celery Beat used for running periodic tasks"""

# Third Party
from datetime import timedelta

# Services
from app.api.services import celery_scheduler

celery_scheduler.conf.beat_schedule = {


    'complete-pending-transactions': {
        'task': 'complete-pending-transactions',
        'schedule': timedelta(minutes=1),
    },
}
