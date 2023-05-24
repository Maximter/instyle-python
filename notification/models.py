from django.db import models
from post.models import Post
from signup.models import User


class NotificationManager(models.Manager):
    def create(self, recipient, sender, notification_type, post):
        created = self.create(recipient=recipient, sender=sender, notification_type=notification_type, post=post)
        return created


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = NotificationManager()

    class Meta:
        db_table = 'notification'
