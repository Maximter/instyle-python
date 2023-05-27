import random
from django.http import JsonResponse
from django.shortcuts import render
from post.models import Post
from recommendation.service import get_keywords, get_popular_posts, get_recommended_post
from signup.models import User, UserProfile
from django.forms.models import model_to_dict
from django.db.models import Q

from user.service import get_user_by_token


def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    keywords = get_keywords(user)
    recommended_posts = get_recommended_post(keywords)
    if len(recommended_posts) < 15:
        recommended_posts = recommended_posts | get_popular_posts(15-len(recommended_posts))

    context = {
        'user': user,
        'profile': profile,
        'posts': recommended_posts 
    }
    return render(request, 'recommendation/index.html', context)


def search(request, username):
    try:
        user_model = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user_model)
        user = model_to_dict(user_model)
        user['avatar'] = True if profile.avatar_small else False
    except User.DoesNotExist:
        return JsonResponse({})

    return JsonResponse({'user': user})
