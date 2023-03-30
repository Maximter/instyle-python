from django.http import HttpResponseRedirect
from django.shortcuts import render
from .service import delete_relation, follow_db, get_followers, get_followings, get_posts, get_posts_for_other, get_user_by_token, get_owner, is_follower

def index(request):
    response = HttpResponseRedirect('/')
    return response


def user_page(request, username):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    owner = get_owner(username)
    if owner is None:
        return render(request, 'error/404.html')
    
    user.owner = user.id == owner.id
    if user.owner:
        posts = get_posts(owner)
    else:
        user.is_follower = is_follower(user, owner)
        posts = get_posts_for_other(user, owner)
    owner.followers = get_followers(owner)
    owner.followings = get_followings(owner)
    owner.count_post = len(posts)
    owner.count_followers = len(owner.followers)
    owner.count_followings = len(owner.followings)
    
    context = {
        'user': user,
        'owner': owner,
        'posts': posts,
    }
    return render(request, 'user/index.html', context)


def follow(request, username):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    owner = get_owner(username)

    if owner is None or user == owner:
        return
    follow_db(user, owner)
    return HttpResponseRedirect(f'/user/{owner.username}')

def unfollow(request, username):
    owner = get_user_by_token(request.COOKIES.get('instyle_token'))
    user = get_owner(username)
    
    follow_db(user, owner)
    return HttpResponseRedirect(f'/user/{owner.username}')
