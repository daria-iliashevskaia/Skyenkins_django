import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Skyenkins_django.settings')

app = Celery('Skyenkins_django', broker='redis://redis:6379/0',
             backend='redis://redis:6379/0', include=['filechecker.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every': {
        'task': 'filechecker.tasks.file_check',
        'schedule': crontab(minute='*/1'),
    },
}