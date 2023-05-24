from django.shortcuts import render
from notification.models import Notification
from signup.models import UserProfile

from user.service import get_user_by_token


# Create your views here.
def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    notifications = Notification.objects.filter(recipient=user).order_by('-id')[:30]
    return render(request, 'notification/index.html', context={'user': user, 'profile': profile, 'notifications': notifications})
