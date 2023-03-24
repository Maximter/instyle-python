import re
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from signup.models import Token, User
from django.contrib.auth.hashers import check_password


def check_user_exist(user):
    regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    is_email = re.match(regex_email, user['username'])

    user_model = {}
    user_exist = {}
    if is_email:
        try:
            user_model = User.objects.get(email=user['username'])
        except User.DoesNotExist:
            user_model = None
    else:
        try:
            user_model = User.objects.get(username=user['username'])
        except User.DoesNotExist:
            user_model = None
        
    if user_model is None or not check_password(user['password'], user_model.password):
        user_exist = {
        'user': user,
        'user_model': user_model,
        'valid' : False,
        'err': 'Введен неверный логин или пароль',
        'warn': '',
        }
    else:
        user_exist = {
        'user': user,
        'user_model': user_model,
        'valid' : True,
        'err': '',
        'warn': '',
        }
    # if user_model.verificated == 0:
    #     #TODO Снова отправить письмо на почту
    #     user_exist = {
    #     'user': user,
    #     'valid' : False,
    #     'err': '',
    #     'warn': 'Ваш эл. адрес не был подтверждён. Для получения доступа к сервису перейдите по ссылке из отправленного письма',
    #     }
    
    return user_exist

def get_token(user):
    token = Token.objects.get(user=user.id)
    return token.token