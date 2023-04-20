from django.shortcuts import render
from settings.forms import AvatarForm
from settings.service import edit_profile_data, save_avatar, update_password
from signup.models import UserProfile
from user.service import get_user_by_token
from django.http import QueryDict
from django.shortcuts import redirect
from django.contrib import messages

def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    form = AvatarForm()
    return render(request, 'settings/index.html', context = {'user': user, 'form': form, 'profile':profile,})

def edit_profile(request):
    user_old = get_user_by_token(request.COOKIES.get('instyle_token'))
    user = {
        'name_lastname': request.POST.get('name_lastname'),
        'username': request.POST.get('username'),
        'email': request.POST.get('email'),
        'bio': request.POST.get('bio'),
    }
    response = edit_profile_data(user, user_old)
    if response['err']:
        messages.error(request, response['err'])
    else:
        messages.success(request, response['success'])
    return redirect('/settings')

def change_avatar(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    form = AvatarForm(request.POST, request.FILES)
    response = save_avatar(user, form)
    if response['err']:
        messages.error(request, response['err'])
    else:
        messages.success(request, response['success'])
    return redirect('/settings')

def change_password(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    passwords = {
        'old_pass': request.POST.get('old-pass'),
        'new_pass': request.POST.get('new-pass'),
        'new_pass2': request.POST.get('new-pass2'),
    }
    response = update_password(passwords, user)
    if response['err']:
        messages.error(request, response['err'])
    else:
        messages.success(request, response['success'])
    return redirect('/settings')