import re

import requests
from signup.models import Token, User
from django.contrib.auth.hashers import check_password
import hashlib
from django.core.mail import send_mail
from django.conf import settings
import asyncio
from django.contrib.auth.hashers import make_password
import uuid
from django.db import connection



def check_user_exist(user):
    user_model = {}
    user_exist = {}
    try:
        user_model = User.objects.get(username=user['username'])
    except User.DoesNotExist:
        user_model = None
        
    if user_model is None or not check_password(user['password'], user_model.password):
        user_exist = {
        'user': user,
        'user_model': user_model,
        'valid' : False,
        'err': 'Введено неверное имя пользователя или пароль',
        'warn': '',
        }
    elif user_model.verificated == 0:
        send_mail_func(user_model)
        user_exist = {
        'user': user,
        'valid' : False,
        'err': '',
        'warn': 'Ваш эл. адрес не был подтверждён. Для получения доступа к сервису перейдите по ссылке из отправленного письма',
        }
    else:
        user_exist = {
        'user': user,
        'user_model': user_model,
        'valid' : True,
        'err': '',
        'warn': '',
        }
    
    
    return user_exist

def get_token(user):
    try:
        token = Token.objects.get(user=user.id)
    except Token.DoesNotExist:
        return None
    return token.token

def send_mail_func(user):
    key = hashlib.sha1((user.email).encode('utf-8')).hexdigest()
    Token.objects.filter(user=user.id).update(confirmation_key=key)
    subject = 'Подтверждение регистрации'
    message = f'Для подтверждения регистрации перейдите по ссылке: {settings.BASE_URL}/login/confirm?key={key}'
    from_email = 'm-a-x-o-k@yandex.ru'
    recipient_list = [user.email,]
    send_mail(subject, message, from_email, recipient_list)

def get_yandex_token(code):
    body = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET
    }
    response = requests.post('https://oauth.yandex.ru/token', body)
    return response.json()

def get_yandex_user(data):
    params = f'jwt_secret={settings.JWT_SECRET}&oauth_token={data["access_token"]}'
    response = requests.get(f'https://login.yandex.ru/info?{params}')
    return response.json()

def valid_password(password):
    if len(password) < 8:
        return 'Введен слишком короткий пароль'
    elif len(password) > 65:
        return 'Введен слишком длинный пароль'
    
def save_new_password(user, password):
    hash_password = make_password(password)
    user = User.objects.get(id=user.id)
    user.password=hash_password
    user.save()
    return