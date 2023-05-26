from notification.models import Notification


def send_notification(recipient, sender, notification_type, post=None):
    if post is None:
        notification = Notification(recipient=recipient, sender=sender, notification_type=notification_type,)
    else:
        notification = Notification(recipient=recipient, sender=sender, notification_type=notification_type, post=post)
    notification.save()


def delete_notification(recipient, sender, notification_type, post=None):
    if post is None:
        notification = Notification.objects.filter(recipient=recipient, sender=sender, notification_type=notification_type,)
    else:
        notification = Notification.objects.filter(recipient=recipient, sender=sender, notification_type=notification_type, post=post)
    notification[0].delete()
