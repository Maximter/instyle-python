from notification.service import delete_notification, send_notification
from post.models import Favorite, Post
from signup.models import Token, User
from django.db.models import Q
from django.db.models.signals import post_save

from user.models import Blacklist, Follow
from django.dispatch import receiver

def get_user_by_token(token):
    try:
        token_model = Token.objects.get(token=token)
    except Token.DoesNotExist:
        return None
    return token_model.user


def get_owner(username):
    try:
        owner = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    return owner


def get_posts_for_other(user, owner):
    try:
        if user.is_follower:
            posts = Post.objects.filter(Q(user=owner) & (Q(visibility='all') | Q(visibility='follower'))).order_by('-id')
        else:
            posts = Post.objects.filter(Q(user=owner) & Q(visibility='all')).order_by('-id')
    except User.DoesNotExist:
        return None
    return posts


def follow_db(follower, following):
    try:
        realtion = Follow.objects.filter(follower=follower, following=following)
        if len(realtion) == 0:
            raise Follow.DoesNotExist
        realtion.delete()
        delete_notification(following, follower, 'follow')
    except Follow.DoesNotExist:
        Follow.objects.create_post(follower=follower, following=following,)
        send_notification(following, follower, 'follow')
    return realtion


def is_follower(follower, following):
    try:
        Follow.objects.get(follower=follower, following=following)
        return True
    except Follow.DoesNotExist:
        return False
    
def is_banned(user, owner):
    try:
        Blacklist.objects.get(user=user, blocked_user=owner)
        return True
    except Blacklist.DoesNotExist:
        return False
    

@receiver(post_save, sender=Blacklist)
def unfollow_if_banned(sender, instance, created, **kwargs):
    # Check if a new Blacklist entry is created
    if created:
        blocking_user = instance.user
        blocked_user = instance.blocked_user

        # Check if the blocking user is following the blocked user
        follow_entry = Follow.objects.filter(follower=blocking_user, following=blocked_user).first()
        if follow_entry:
            follow_entry.delete()

        # Check if the blocked user is following the blocking user
        follow_entry = Follow.objects.filter(follower=blocked_user, following=blocking_user).first()
        if follow_entry:
            follow_entry.delete()


def get_followers(user):
    try:
        return Follow.objects.filter(following=user)
    except Follow.DoesNotExist:
        return []


def get_followings(user):
    try:
        return Follow.objects.filter(follower=user)
    except Follow.DoesNotExist:
        return []


def get_posts(user):
    try:
        posts = Post.objects.filter(~Q(visibility='nobody'), user=user,).order_by('-id')
    except Post.DoesNotExist:
        return None
    return posts

def get_archive(user):
    try:
        posts = Post.objects.filter(visibility='nobody', user=user,).order_by('-id')
    except Post.DoesNotExist:
        return None
    return posts

def get_favorite(user):
    try:
        posts = Favorite.objects.filter(user=user,).order_by('-id')
    except Favorite.DoesNotExist:
        return None
    return posts
