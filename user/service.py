from post.models import Post
from signup.models import Token, User
from django.db.models import Q

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
        # Если подписан, то другая функция TODO
        # if user.follower:
            # posts = Post.objects.filter(Q(user=owner) & Q(visibility='all') | Q(visibility='follower')).order_by('-id')
        # else:
        posts = Post.objects.filter(Q(user=owner) & Q(visibility='all')).order_by('-id')
    except User.DoesNotExist:
        return None
    return posts

def get_posts(user):
    try:
        posts = Post.objects.filter(user=user).order_by('-id')
    except User.DoesNotExist:
        return None
    return posts