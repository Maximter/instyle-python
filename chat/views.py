from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from chat.models import ChatRoom, Message
from signup.models import User, UserProfile
from django.db.models import Q

from user.service import get_user_by_token

# Create your views here.
from django.db.models import F

def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    chat_rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user)).annotate(
        last_message_timestamp=F('message__timestamp')
    ).order_by('-last_message_timestamp')

    context = {
        'user': user,
        'profile': profile,
        'chats': []
    }
    for chat_room in chat_rooms:
        if user == chat_room.user1:
            avatar_user = UserProfile.objects.filter((~Q(avatar_small='') & ~Q(avatar_small='static/img/small/avatar/standard.png')) & Q(user=chat_room.user2))
            username = chat_room.user2.username
            user_id = chat_room.user2.id
        else:
            avatar_user = UserProfile.objects.filter((~Q(avatar_small='') & ~Q(avatar_small='static/img/small/avatar/standard.png')) & Q(user=chat_room.user1))
            username = chat_room.user1.username
            user_id = chat_room.user1.id
        if not any(chat['room_identifier'] == chat_room.room_identifier for chat in context['chats']):
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
        return JsonResponse([], safe=False)

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