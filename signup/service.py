import re
from .models import User, Token
from django.contrib.auth.hashers import make_password

def valid_user(user: User): 
    if not user['email'] or not user['name_lastname'] or not user['username'] or not user['password']:
        return 'Введены не все поля для регистрации пользователя'

    validEmail = re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', user['email'])
    if not validEmail:
        return 'Введен неверный эл. адрес'
    
    validNameLastname = re.match(r'^[A-Za-zА-Яа-я ]+$', user['name_lastname'])
    if not validNameLastname:
        return 'Имя и фамилия должны содержать только буквы'
    
    if len(user['password']) < 8:
        return 'Введен слишком короткий пароль'
    elif len(user['password']) > 65:
        return 'Введен слишком длинный пароль'
    
    if len(user['name_lastname']) < 4:
        return 'Слишком короткое имя и фамилия'
    elif len(user['name_lastname']) > 30:
        return 'Слишком длинное имя и фамилия'
    
    if len(user['username']) < 4:
        return 'Слишком короткое имя пользователя'
    elif len(user['username']) > 30:
        return 'Слишком длинное имя пользователя'
    
    existEmail = User.objects.filter(email=user['email'])
    if not len(existEmail) == 0:
        return 'Введенная почта принадлежит другому пользователю'
    
    existUsername = User.objects.filter(username=user['username'])
    if not len(existUsername) == 0:
        return 'Введенное имя пользователя уже занято'
    
    return ''

def create_user(user):
    hash_password = make_password(user['password'])
    user = User.objects.create_user(email = user['email'], name_lastname = user['name_lastname'], 
                                    username = user['username'], password = hash_password)
    Token.objects.create_token(user = user)
    return