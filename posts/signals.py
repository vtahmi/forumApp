from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_approval_email_notification

from forumApp.settings import DEFAULT_EMAIL
from posts.models import Post

@receiver(signal=post_save, sender=Post)
def send_approval_email(sender, instance, created, **kwargs):
    if created:
        send_approval_email_notification.delay(
            subject="Post Approval",
            message="Your post has been approved",
            recipient_list=[instance.author.email],
            from_email=DEFAULT_EMAIL,

        )
