import io
import re
from login.service import send_mail_func
from .models import User, Token, UserProfile
from django.contrib.auth.hashers import make_password
import random
import string
import urllib.request
from django.core.files import File
from django.core.mail import send_mail


def create_user_and_token(form):
    user = form.save(commit=False)
    user.verificated = False
    user.password = make_password(user.password)
    user.save()
    UserProfile.objects.create_profile(user)
    Token.objects.create_token(user=user)
    return user


def save_yandex_user(user):
    user['password'] = generate_password()
    hash_password = make_password(user['password'])
    try:
        User.objects.get(username=user['login'])
        user['login'] = generate_password(10)
    except User.DoesNotExist:
        pass

    user_model = User.objects.create_user(email=user['default_email'], name_lastname=user['real_name'],
                                          username=user['login'], password=hash_password, verificated=True)
    Token.objects.create_token(user=user_model)
    if not user['is_avatar_empty']:
        download_avatar(user['default_avatar_id'], user_model)

    send_password(user)
    return user_model


def download_avatar(avatar, user):
    big_url = f'https://avatars.yandex.net/get-yapic/{avatar}/islands-200'
    small_url = f'https://avatars.yandex.net/get-yapic/{avatar}/islands-retina-50'
    big_response = urllib.request.urlopen(big_url)
    small_response = urllib.request.urlopen(small_url)
    big_image = big_response.read()
    small_image = small_response.read()
    profile = UserProfile.objects.get(user=user)
    profile.avatar_big = File(io.BytesIO(big_image), user.id)
    profile.avatar_small = File(io.BytesIO(small_image), user.id)
    profile.save()


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def send_password(user):
    subject = 'Регистрация'
    message = f'Временный пароль: {user["password"]}'
    from_email = 'm-a-x-o-k@yandex.ru'
    recipient_list = [user["default_email"]]
    send_mail(subject, message, from_email, recipient_list)
