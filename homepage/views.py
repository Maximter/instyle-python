from django.shortcuts import render
from homepage.service import get_post_like_count, get_posts_in_homepage, get_user_post_interaction
from recommendation.service import get_popular_posts
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
    return render(request, 'homepage/index.html', context = {'user': user, 'posts': posts, 'profile': profile, 'recommendation': recommendation})

def get_posts(user, start=0):
    posts = get_posts_in_homepage(user, start)
    posts = get_post_like_count(posts) 
    posts = get_user_post_interaction(user, posts)
    return posts

def get_popular_posts_homepage(user):
    posts = get_popular_posts()
    posts = get_post_like_count(posts) 
    posts = get_user_post_interaction(user, posts)
    return posts