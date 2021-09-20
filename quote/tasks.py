from celery import shared_task
from django_celery_beat.models import PeriodicTask



@shared_task
def take_quote():
    pass
