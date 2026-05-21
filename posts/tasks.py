import time

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_approval_email_notification(subject, message, from_email, recipient_list):
    time.sleep(5)
    send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=from_email,
    )

