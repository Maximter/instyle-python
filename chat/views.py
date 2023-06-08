from django.shortcuts import render
from signup.models import UserProfile

from user.service import get_user_by_token

# Create your views here.
def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    return render(request, 'chat/index.html', context={'user': user, 'profile': profile})
