import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from chat.models import ChatRoom, Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test' 

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({
            'channel': self.channel_name,
            'type':'channel',
        }))
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        channel_name = self.channel_name

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'sender_id':sender_id,
                'channel_name': channel_name
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        channel_name = event['channel_name']

        self.send(text_data=json.dumps({
            'type':'message',
            'message':message,
            'sender_id':sender_id,
            'channel_name':channel_name
        }))

    def save_message(self, sender_id, message):
        # Find the chat room
        chat_room = ChatRoom.objects.get(room_identifier=self.room_group_name)

        # Create the message object and save it to the database
        message = Message.objects.create(
            sender_id=sender_id,
            receiver_id=chat_room.user2_id if chat_room.user1_id == sender_id else chat_room.user1_id,
            content=message,
            chat_room=chat_room
        )
        message.save()