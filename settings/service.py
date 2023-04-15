from post.models import Comment, Like, Post
from user.models import Follow
from django.db.models import Q


def get_post_like_count(posts):
    #TODO REDO
    try:
        for this in posts:
            this.like_count = len(Like.objects.filter(post=this.id))
    except Comment.DoesNotExist or Like.DoesNotExist:
        pass
    return posts
