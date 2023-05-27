import random
from django.utils import timezone
from django.db.models import Count
from django.core.cache import cache

from post.models import Post


def get_popular_posts(count):
    now = timezone.now()
    month_ago = now - timezone.timedelta(days=30)
    popular_posts = Post.objects.filter(date_post__gte=month_ago, visibility='all')\
                        .annotate(num_likes=Count('likes'))\
                        .order_by('-num_likes', '-date_post')[:count]

    return popular_posts


def get_keywords(user):
    cache_key = f"keywords_{user.id}"
    keywords = cache.get(cache_key)
    if keywords is None:
        now = timezone.now()
        year_ago = now - timezone.timedelta(days=365)
        four_month_ago = now - timezone.timedelta(days=120)
    
        liked_posts = Post.objects.filter(likes__user=user, likes__liking_date__gte=four_month_ago)
        user_posts = Post.objects.filter(user=user, date_post__gte=year_ago)

        posts = liked_posts | user_posts

        keywords = [post.keywords.split(',') for post in posts]
        flattened_keywords = [keyword.strip() for sublist in keywords for keyword in sublist if keyword]

        keyword_frequencies = dict()
        for keyword in flattened_keywords:
            keyword_frequencies[keyword] = keyword_frequencies.get(keyword, 0) + 1

        keywords = sorted(keyword_frequencies, key=keyword_frequencies.get, reverse=True)
        
        cache.set(cache_key, keywords, timeout=300)

    return keywords

def get_recommended_post(sorted_keywords):
    if sorted_keywords:
        recommended_posts = Post.objects.filter(keywords__icontains=sorted_keywords[0])
        for keyword in sorted_keywords[1:]:
            recommended_posts |= Post.objects.filter(keywords__icontains=keyword)

        recommended_posts = recommended_posts.order_by('-id').distinct()[:35]

        recommended_posts = list(recommended_posts)
        random.shuffle(recommended_posts)

        num_posts = min(15, len(recommended_posts))
        recommended_posts = recommended_posts[:num_posts]
        recommended_posts = Post.objects.filter(id__in=[post.id for post in recommended_posts])
    else:
        return Post.objects.none()

    return recommended_posts