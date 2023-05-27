from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from signup.models import User, UserProfile
from user.models import Blacklist
from .service import follow_db, get_archive, get_favorite, get_followers, get_followings, get_posts, get_posts_for_other, get_user_by_token, get_owner, is_banned, is_follower
from django.contrib import messages

def index(request):
    return HttpResponseRedirect('/')


def user_page(request, username):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = get_object_or_404(UserProfile, user=user)
    owner = get_owner(username)

    if owner is None:
        return render(request, 'error/404.html')

    user.is_owner = user.id == owner.id

    if user.is_owner:
        posts = get_posts(owner)
        archive = get_archive(owner)
        favorite = get_favorite(owner)
        user.is_banned = False
    else:
        user.is_follower = is_follower(user, owner)
        archive = None
        favorite = None
        posts = get_posts_for_other(user, owner)
        owner.is_banned = is_banned(user, owner)
        user.is_banned = is_banned(owner, user)

    if not user.is_banned:
        owner.followers = get_followers(owner)
        owner.followings = get_followings(owner)
        owner.count_post = len(posts)
        owner.count_followers = len(owner.followers)
        owner.count_followings = len(owner.followings)
        owner_profile = UserProfile.objects.get(user=owner.id)
    else:
        posts = []
        owner_profile = None

    context = {
        'user': user,
        'owner': owner,
        'owner_profile': owner_profile,
        'posts': posts,
        'profile': profile,
        'archive': archive,
        'favorite': favorite
    }
    return render(request, 'user/index.html', context)


def block_user(request, user_id):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    referer = request.META.get('HTTP_REFERER')

    try:
        user_to_block = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Такого пользователя не существует")
        return redirect(referer)

    if user_to_block == request.user:
        messages.error(request, "Вы не можете заблокировать сами себя")
        return redirect(referer)

    try:
        blacklist_entry = Blacklist.objects.get(user=user, blocked_user=user_to_block)
        blacklist_entry.delete()
        messages.success(request, f"Вы разблокировали {user_to_block.username}")
    except Blacklist.DoesNotExist:
        blacklist_entry = Blacklist(user=user, blocked_user=user_to_block)
        blacklist_entry.save()
        messages.success(request, f"Вы заблокировали {user_to_block.username}")
    
    return redirect(referer)


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
