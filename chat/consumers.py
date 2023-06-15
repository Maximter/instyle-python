import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from chat.models import ChatRoom, Message
from signup.models import User
from user.models import Blacklist

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name'] 

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
        receiver_id = text_data_json['receiver_id']
        channel_name = self.channel_name

        if self.is_blocked(sender_id, receiver_id):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'error',
                    'message':'Вы были заблокированы пользователем',
                    'channel_name': channel_name
                }
            )
            return
        elif self.blocked(sender_id, receiver_id):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'error',
                    'message':'Вы не можете писать заблокированному пользователю',
                    'channel_name': channel_name
                }
            )
            return
        

        self.save_message(sender_id, receiver_id, message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'sender_id':sender_id,
                'receiver_id':receiver_id,
                'channel_name': channel_name
            }
        )

    def error(self, event):
        message = event['message']
        channel_name = event['channel_name']

        self.send(text_data=json.dumps({
            'type':'error',
            'message':message,
            'channel_name': channel_name
        }))

    
    
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

    def is_blocked(self, sender_id, receiver_id):
        user = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        is_blocked = Blacklist.objects.filter(user=receiver, blocked_user=user).first()
        if is_blocked:
            return True
        return False
    
    def blocked(self, sender_id, receiver_id):
        user = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        is_blocked = Blacklist.objects.filter(user=user, blocked_user=receiver).first()
        if is_blocked:
            return True
        return False

    def save_message(self, sender_id, receiver_id, message):
        # Find the chat room
        chat_room = ChatRoom.objects.filter(room_identifier=self.room_group_name).first()
        if not chat_room:
            chat_room = self.create_room(sender_id, receiver_id)

        # Create the message object and save it to the database
        message = Message.objects.create(
            sender_id=sender_id,
            receiver_id=chat_room.user2_id if chat_room.user1_id == sender_id else chat_room.user1_id,
            content=message,
            chat_room=chat_room
        )
        message.save()

    def create_room(self, user_id, receiver_id):
        sorted_ids = sorted([user_id, receiver_id])
        room_identifier = f'room_{sorted_ids[0]}_{sorted_ids[1]}'
        user = User.objects.get(id=user_id)
        receiver = User.objects.get(id=receiver_id)
        chat_room = ChatRoom.objects.create(user1=user, user2=receiver, room_identifier=room_identifier)
        return chat_room