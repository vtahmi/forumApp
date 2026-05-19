import time

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from forumApp.settings import DEFAULT_EMAIL
from posts.models import Post


def send_approval_email(subject, message, from_email, recipient_list):
    time.sleep(5)
    send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=from_email,
    )



@receiver(signal=post_save, sender=Post)
def send_approval_email(sender, instance, created, **kwargs):
    if created:
        send_approval_email(
            subject="Post Approval",
            message="Your post has been approved",
            recipient_list=[instance.author.email],
            from_email=DEFAULT_EMAIL,

        )
