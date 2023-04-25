from django.http import HttpResponse
from django.shortcuts import render
from instyle import settings

from post.service import check_valid_post, save_post_to_db, save_posts_from_vk, upload_post
from signup.models import UserProfile
from user.service import get_user_by_token
from django.shortcuts import redirect
from django.contrib import messages
from asgiref.sync import async_to_sync, sync_to_async

import requests
import asyncio

import re

def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    return render(request, 'post/index.html', context={'user':user, 'profile':profile})


def create(request):
    comment = request.POST.get('comment')
    if comment is not None:
        comment = comment.strip() 
    user = get_user_by_token(request.COOKIES.get('instyle_token'))

    if request.method == 'POST' and request.FILES:
        file = request.FILES['photo'] 

        valid_post = check_valid_post(file, comment)
        if valid_post['err']:
            messages.error(request, valid_post['err'])
            return redirect('/post')
        
        id_post = upload_post(file, user)
        save_post_to_db(id_post, comment, user)
        messages.success(request, 'Пост будет опубликован через несколько секунд')
        return redirect('/post')
    messages.error(request, 'Ошибка файла')
    return redirect('/post')

def get_vk_token(request):
    return render(request, 'post/vk_token.html',)

def get_vk_photos(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    body = str(request.body)
    start = "access_token="
    end = "&"
    start_idx = body.find(start) + len(start)
    end_idx = body.find(end, start_idx)
    access_token = body[start_idx:end_idx].strip()
    response = requests.post(f'https://api.vk.com/method/photos.getAll?access_token={access_token}&v=5.131&count=200')
    response = response.json()
    save_posts_from_vk(response, user)
    messages.success(request, 'Посты будут загружены и опубликованы в ближайшее время')
    return redirect('/settings')

