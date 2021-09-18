from celery import shared_task

from django.core.mail import send_mail


@shared_task
def need_send_mail(email, text):
    send_mail('Remind me', text, 'admin@mail.com', [email])
