import re
from signup.models import Token, User
from django.contrib.auth.hashers import check_password


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