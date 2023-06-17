import uuid
from django.db import models
import os


def upload_small_avatar(instance, filename):
    path = f'static/img/small/avatar/{filename}.jpg'
    if os.path.exists(path):
        os.remove(path)

    return path


def upload_medium_avatar(instance, filename):
    path = f'static/img/medium/avatar/{filename}.jpg'
    if os.path.exists(path):
        os.remove(path)

    return path


def upload_big_avatar(instance, filename):
    path = f'static/img/big/avatar/{filename}.jpg'
    if os.path.exists(path):
        os.remove(path)

    return path


class User(models.Model,):
    email = models.CharField(unique=True, max_length=45)
    name_lastname = models.CharField(max_length=40)
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=105)
    verificated = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    message_visibility = models.CharField(max_length=30, default='all')

    class Meta:
        db_table = 'user'


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=300, default='')
    avatar_small = models.ImageField(upload_to=upload_small_avatar, blank=False)
    avatar_big = models.ImageField(upload_to=upload_big_avatar, blank=False)

    class Meta:
        db_table = 'userProfile'


class Token(models.Model,):
    token = models.CharField(max_length=40, default=uuid.uuid4, unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    confirmation_key = models.CharField(max_length=60, blank=True)

    class Meta:
        db_table = 'token'
