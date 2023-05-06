from django.shortcuts import render
from instyle import settings
from settings.forms import AvatarForm
from settings.service import edit_profile_data, save_avatar, update_password
from signup.models import Token, UserProfile
from signup.service import generate_password
from user.service import get_user_by_token
from django.http import HttpResponse, QueryDict
from django.shortcuts import redirect
from django.contrib import messages
import hashlib
from django.core.mail import send_mail
from django.template.loader import render_to_string

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

def delete_user(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    user.delete()
    return HttpResponse()

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


def forgot_password(request, user=None):
    redirect_url = '/login'
    if user is None:
        user = get_user_by_token(request.COOKIES.get('instyle_token'))
        redirect_url = '/settings'
    key = hashlib.sha1(generate_password(15).encode('utf-8')).hexdigest()
    Token.objects.filter(user=user.id).update(confirmation_key=key)
    subject = 'Изменение пароля'
    link = f'{settings.BASE_URL}/login/change-forgot-password-page?key={key}'
    html_message = render_to_string('email/reset_password.html', {'link': link}) 
    from_email = 'm-a-x-o-k@yandex.ru'
    recipient_list = [user.email,]
    send_mail(subject=subject, message='', from_email=from_email, recipient_list=recipient_list, html_message=html_message)
    messages.success(request, 'Ссылка по восстановлению пароля была отправлена на Ваш email')
    return redirect(redirect_url)