from post.models import Comment, Like, Post
from user.models import Follow
from django.db.models import Q

def get_posts_in_homepage(user, start):
    try:
        followings = Follow.objects.values_list('following', flat=True).filter(follower=user)
    except Follow.DoesNotExist:
        return None

    try:
        posts = \
            Post.objects.filter(Q(user_id__in=followings) & \
                                ~Q(visibility='nobody') & \
                                ~Q(visibility='link') | \
                                Q(user=user.id)).order_by('-id')[start:10]
    except Post.DoesNotExist:
        return None
    return posts


def get_post_like_count(posts):
    #TODO REDO
    try:
        for this in posts:
            this.like_count = len(Like.objects.filter(post=this.id))
    except Comment.DoesNotExist or Like.DoesNotExist:
        pass
    return posts

def get_user_post_interaction(user, posts):
    #TODO REDO
    for this in posts:
            this.owner = user.id == this.user.id
            try:
                this.user_like = Like.objects.get(user=user.id, post=this.id)
            except Like.DoesNotExist:
                pass
    return posts