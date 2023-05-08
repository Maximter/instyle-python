from django.utils import timezone
from django.db.models import Count

from post.models import Post


def get_popular_posts():
    now = timezone.now()
    month_ago = now - timezone.timedelta(days=30)
    popular_posts = Post.objects.filter(date_post__gte=month_ago, visibility='all')\
                        .annotate(num_likes=Count('likes'))\
                        .order_by('-num_likes', '-date_post')[:18]
    return popular_posts
