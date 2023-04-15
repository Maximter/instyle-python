from django.shortcuts import render
from user.service import get_user_by_token

def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    return render(request, 'settings/index.html', context = {'user': user,})

