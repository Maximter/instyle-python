import json
from django.http import HttpResponse
from django.shortcuts import render
from homepage.service import get_post_like_count, get_posts_in_homepage,\
    get_user_post_interaction
from instyle import settings
from recommendation.service import get_keywords, get_popular_posts, get_recommended_post
from signup.models import UserProfile
from user.service import get_user_by_token


def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    posts = get_posts(user)
    recommendation = False
    if len(posts) == 0:
        posts = get_popular_posts_homepage(user)
        recommendation = True
    base_url = settings.BASE_URL
    context = {
        'user': user,
        'posts': posts,
        'profile': profile,
        'recommendation': recommendation,
        'base_url': base_url
    }
    return render(request, 'homepage/index.html', context)


def get_recommendation(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    keywords = get_keywords(user)
    posts = get_recommended_post(keywords)
    if len(posts) < 15:
        posts = posts | get_popular_posts(15-len(posts))
    posts = get_post_like_count(posts)
    posts = get_user_post_interaction(user, posts)

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


def get_posts(user, start=0):
    posts = get_posts_in_homepage(user, start)
    posts = get_post_like_count(posts)
    posts = get_user_post_interaction(user, posts)
    return posts


def get_popular_posts_homepage(user):
    keywords = get_keywords(user)
    posts = get_recommended_post(keywords)
    if len(posts) < 15:
        posts = posts | get_popular_posts(15-len(posts))
    posts = get_post_like_count(posts)
    posts = get_user_post_interaction(user, posts)
    return posts
