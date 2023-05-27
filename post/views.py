from django.http import HttpResponse
from django.shortcuts import render
import json
from homepage.views import get_posts
from post.service import check_valid_post, get_image_keywords, save_post_to_db, save_posts_from_vk, upload_post
from signup.models import UserProfile
from user.service import get_user_by_token
from django.shortcuts import redirect
from django.contrib import messages
from vk_downloads import download
from django.core import serializers
from django.db.models import Model

from datetime import datetime

import requests


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Model):
            return obj.__dict__
        return super().default(obj)



def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    return render(request, 'post/index.html', context={'user': user, 'profile': profile})


def create(request):
    comment = request.POST.get('comment')
    visibility = request.POST.get('visibility')
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
        keywords = get_image_keywords(user, id_post)
        save_post_to_db(id_post, comment, user, visibility, keywords)
        messages.success(request, 'Пост будет опубликован через несколько секунд')
        return redirect('/post')
    messages.error(request, 'Ошибка файла')
    return redirect('/post')


def get_more(request): 
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    start = request.GET.get('start')
    posts = get_posts(user, start)

    serialized_posts = []
    for post in posts:
        serialized_post = {
            'id_post': post.id_post,
            'comment': post.comment,
            'hide_like': post.hide_like,
            'avatar': post.avatar,
            'user_like': post.user_like,
            'like_count': post.like_count,
            'user': {
                'id': post.user.id,
                'name_lastname': post.user.name_lastname,
                'username': post.user.username,
            },
        }
        serialized_posts.append(serialized_post)

    json_data = json.dumps(serialized_posts)
    response = HttpResponse(json_data, content_type='application/json')
    
    return response

def get_vk_token(request):
    return render(request, 'post/vk_token.html',)


def get_vk_photos(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    if user.id not in download:
        download[user.id] = True
    else:
        return HttpResponse()
    access_token = get_access_token(request)
    url = f'https://api.vk.com/method/photos.getAll?access_token={access_token}&v=5.131&count=200'
    response = requests.post(url).json()
    save_posts_from_vk(response, user)
    messages.success(request, 'Все посты были успешно загружены')
    del download[user.id]
    return HttpResponse()


def get_access_token(request):
    body = str(request.body)
    start = "access_token="
    end = "&"
    start_idx = body.find(start) + len(start)
    end_idx = body.find(end, start_idx)
    return body[start_idx:end_idx].strip()
