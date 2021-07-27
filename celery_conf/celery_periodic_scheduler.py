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
    'list-minted-tokens': {
        'task': 'list-minted-tokens',
        'schedule': timedelta(minutes=1),
    },
    'assign-nfts-to-user': {
        'task': 'assign-nfts-to-user',
        'schedule': timedelta(minutes=1),
    },
}
