from django.shortcuts import render
from homepage.service import get_post_like_count, get_posts_in_homepage,\
    get_user_post_interaction
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
    context = {
        'user': user,
        'posts': posts,
        'profile': profile,
        'recommendation': recommendation
    }
    return render(request, 'homepage/index.html', context)


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
