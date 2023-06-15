from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from chat.models import ChatRoom, Message
from signup.models import User, UserProfile
from django.db.models import Q

from user.service import get_user_by_token

# Create your views here.
def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    chat_rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user))
    context = {
        'user': user,
        'profile': profile,
        'chats': []
    }
    for chat_room in chat_rooms:
        if user == chat_room.user1:
            avatar_user = UserProfile.objects.filter((~Q(avatar_small = '') & ~Q(avatar_small = 'static/img/small/avatar/standard.png')) & Q(user=chat_room.user2))
            username = chat_room.user2.username
            user_id = chat_room.user2.id
        else:
            avatar_user = UserProfile.objects.filter((~Q(avatar_small = '') & ~Q(avatar_small = 'static/img/small/avatar/standard.png')) & Q(user=chat_room.user1))
            username = chat_room.user1.username
            user_id = chat_room.user1.id
        context['chats'].append({
            'room_identifier': chat_room.room_identifier,
            'username': username,
            'user_id': user_id,
            'avatar': avatar_user,
        })
    return render(request, 'chat/index.html', context=context)

def send_message_view(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    return render(request, 'chat/index.html', context={'user': user, 'profile': profile})

def get_messages(request, id_user):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    receiver = get_object_or_404(User, id=id_user)

    try:
        chat_room = ChatRoom.objects.get(Q(user1=user, user2=receiver) | Q(user1=receiver, user2=user))
    except ChatRoom.DoesNotExist:
        sorted_ids = sorted([user.id, receiver.id])
        room_identifier = f'room_{sorted_ids[0]}_{sorted_ids[1]}'
        chat_room = ChatRoom.objects.create(user1=user, user2=receiver, room_identifier=room_identifier)
    messages = Message.objects.filter(chat_room=chat_room)

    message_list = []
    for message in messages:
        message_data = {
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
        }
        message_list.append(message_data)

    return JsonResponse(message_list, safe=False)