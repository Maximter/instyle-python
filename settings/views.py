from django.shortcuts import render
from settings.service import edit_profile_data
from user.service import get_user_by_token

def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    return render(request, 'settings/index.html', context = {'user': user,})

def edit_profile(request):
    user_old = get_user_by_token(request.COOKIES.get('instyle_token'))
    user = {
        'name_lastname': request.POST.get('name_lastname'),
        'username': request.POST.get('username'),
        'email': request.POST.get('email'),
    }
    response = edit_profile_data(user, user_old)
    user_new = get_user_by_token(request.COOKIES.get('instyle_token'))
    return render(request, 'settings/index.html', context = {'user': user_new, 'response': response})

