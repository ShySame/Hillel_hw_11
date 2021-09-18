import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'HW_11.settings')

app = Celery('HW_11')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
