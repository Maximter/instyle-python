from django.db import models

from signup.models import User

class ChatRoom(models.Model):
    room_identifier = models.CharField(max_length=255, unique=True, default='')
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms2')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('timestamp',)

