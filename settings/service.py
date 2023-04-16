from post.models import Comment, Like, Post
from signup.models import User
from user.models import Follow
from django.db.models import Q
import re


def edit_profile_data(user, user_old):
    response = {'err': '', 'warn': '', 'success': ''}
    change = False
    try:
        check_valid_update(user, user_old)
    except Exception as err:
        response['err'] = str(err)
        return response
    
    if not user['name_lastname'] == user_old.name_lastname:
        change = True
        User.objects.filter(id=user_old.id).update(name_lastname=user['name_lastname'])

    if not user['username'] == user_old.username:
        change = True
        User.objects.filter(id=user_old.id).update(username=user['username'])

    #TODO отправить на почту ссылку для изменения email
    
    if change:
        response['success'] = 'Данные профиля были изменены'
    return response
    
def check_valid_update(user, user_old):
    validNameLastname = re.match(r'^[A-Za-zА-Яа-я ]+$', user['name_lastname'])
    print(len(user['username']))
    if not validNameLastname:
        raise Exception('Имя и фамилия должны содержать только буквы')
    if len(user['name_lastname']) < 4:
        raise Exception ('Слишком короткое имя и фамилия')
    elif len(user['name_lastname']) > 30:
        raise Exception('Слишком длинное имя и фамилия')
    if len(user['username']) < 4:
        raise Exception ('Слишком короткое имя пользователя')
    elif len(user['username']) > 30:
        raise Exception ('Слишком длинное имя пользователя')
    

    if not user['username'] == user_old.username:
        try:
            User.objects.get(username=user['username'])
            raise Exception ('Введенное имя пользователя уже занято')
        except User.DoesNotExist:
            pass

    if not user['email'] == user_old.email:
        try:
            User.objects.get(email=user['email'])
            raise Exception ('Введенная почта принадлежит другому пользователю')
        except User.DoesNotExist:
            pass
       