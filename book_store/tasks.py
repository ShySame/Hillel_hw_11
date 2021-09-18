from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail(email, date, text):
    send_mail('Remind me', text, 'admin@mail.com', [email])
