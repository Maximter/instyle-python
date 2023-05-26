from post.models import Like, Post
from signup.models import User, UserProfile
from user.models import Follow
from django.db.models import Count
from django.db.models import Q


def get_posts_in_homepage(user, start):
    try:
        followings = Follow.objects.values_list('following', flat=True).filter(follower=user)
    except Follow.DoesNotExist:
        return None

    try:
        posts = \
            Post.objects.filter(~Q(visibility='nobody') &
                                ~Q(visibility='link') &
                                Q(user_id__in=followings) |
                                ~Q(visibility='nobody') &
                                Q(user=user.id)).order_by('-id').prefetch_related('likes')[start:10]
    except Post.DoesNotExist:
        return None
    return posts


def get_post_like_count(posts):
    return posts.prefetch_related('likes').annotate(like_count=Count('likes'))


def get_user_post_interaction(user, posts):
    # TODO REDO
    for this in posts:
        this.owner = user.id == this.user.id
        user_model = User.objects.get(id=this.user.id)
        this.avatar = True if UserProfile.objects.get(user=user_model).avatar_big else False
        try:
            this.user_like = Like.objects.get(user=user.id, post=this.id)
        except Like.DoesNotExist:
            pass
    return posts
