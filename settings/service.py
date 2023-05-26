import re
from signup.models import User, UserProfile
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from user.models import CloseFriend, Follow
from django.core.exceptions import ObjectDoesNotExist



def edit_profile_data(user, user_old):
    response = {'err': '', 'warn': '', 'success': ''}
    change = False
    try:
        check_valid_update(user, user_old)
    except Exception as err:
        response['err'] = str(err)
        return response

    profile = UserProfile.objects.get(user=user_old.id)
    if not profile.bio == user['bio']:
        change = True
        profile.bio = user['bio']
        profile.save()

    if not user['name_lastname'] == user_old.name_lastname:
        change = True
        User.objects.filter(id=user_old.id).update(name_lastname=user['name_lastname'])

    if not user['username'] == user_old.username:
        change = True
        User.objects.filter(id=user_old.id).update(username=user['username'])

    # TODO отправить на почту ссылку для изменения email

    if change:
        response['success'] = 'Данные профиля были изменены'
    return response


def save_avatar(user, form):
    response = {'err': '', 'warn': '', 'success': ''}
    if form.is_valid():
        photo = form.cleaned_data['photo']
        photo.name = f'{user.id}'
        user_model = User.objects.get(id=user.id)
        profile = UserProfile.objects.get(user=user_model)
        profile.avatar_big = photo
        # TODO resize!
        profile.avatar_small = photo
        profile.save()
    else:
        response['err'] = 'Произошла какая-то ошибка'
        return response
    response['success'] = 'Аватар был изменён'
    return response


def check_valid_update(user, user_old):
    validNameLastname = re.match(r'^[A-Za-zА-Яа-я ]+$', user['name_lastname'])
    if not validNameLastname:
        raise Exception('Имя и фамилия должны содержать только буквы')
    if len(user['name_lastname']) < 4:
        raise Exception('Слишком короткое имя и фамилия')
    elif len(user['name_lastname']) > 30:
        raise Exception('Слишком длинное имя и фамилия')
    if len(user['username']) < 4:
        raise Exception('Слишком короткое имя пользователя')
    elif len(user['username']) > 30:
        raise Exception('Слишком длинное имя пользователя')
    elif len(user['bio']) > 300:
        raise Exception('Слишком описание пользователя')

    if not user['username'] == user_old.username:
        try:
            User.objects.get(username=user['username'])
            raise Exception('Введенное имя пользователя уже занято')
        except User.DoesNotExist:
            pass

    if not user['email'] == user_old.email:
        try:
            User.objects.get(email=user['email'])
            raise Exception('Введенная почта принадлежит другому пользователю')
        except User.DoesNotExist:
            pass


def update_password(passwords, user):
    if not passwords['new_pass'] == passwords['new_pass2']:
        return {'err': 'Новые пароли не совпадают'}
    if not check_password(passwords['old_pass'], user.password):
        return {'err': 'Старый пароль введён неверно'}
    hash_password = make_password(passwords['new_pass'])
    user = User.objects.filter(id=user.id).update(password=hash_password)
    return {'err': '', 'success': 'Пароль был успешно изменён'}


def get_close_friends(user):
    return CloseFriend.objects.filter(user=user).select_related('friend')

def get_followers_not_close(user):
    close_friends = CloseFriend.objects.filter(user=user).values_list('friend_id', flat=True)
    followers = Follow.objects.exclude(follower__in=close_friends).filter(following=user)
    
    return followers