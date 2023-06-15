from django.shortcuts import render
from notification.models import Notification
from signup.models import UserProfile
from django.db.models import Q
from user.service import get_user_by_token


# Create your views here.
def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    notifications = Notification.objects.filter(~Q(sender=user) & Q(recipient=user)).order_by('-id')[:30]

    for this in notifications:
        this.avatar = UserProfile.objects.filter((~Q(avatar_small='') & ~Q(avatar_small='static/img/small/avatar/standard.png')) & Q(user=this.sender))

    return render(request, 'notification/index.html', context={'user': user, 'profile': profile, 'notifications': notifications})
