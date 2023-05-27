from django.db import models
from django.utils import timezone

from signup.models import User


class PostManager(models.Manager):
    def create_post(self, id_post, user, comment, visibility, keywords):
        keywords = ', '.join(keywords)
        post = self.create(id_post=id_post, user=user, comment=comment, visibility=visibility, keywords=keywords)
        return post


class Comment_Manage(models.Manager):
    def create_post(self, post, user, comment_text,):
        post = self.create(post=post, user=user, comment_text=comment_text,)
        return post


class Like_Manage(models.Manager):
    def create_post(self, post, user, ):
        post = self.create(post=post, user=user, )
        return post


class Post(models.Model,):
    id_post = models.CharField(unique=True, max_length=13)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date_post = models.DateTimeField(default=timezone.now)
    hide_like = models.BooleanField(default=False)
    hide_comment = models.BooleanField(default=False)
    comment = models.CharField(max_length=1500)
    keywords = models.TextField(blank=True)
    visibility = models.CharField(max_length=20, default='all')
    objects = PostManager()

    @staticmethod
    def get_posts_by_keywords(keywords):

        posts = Post.objects.filter(keywords__icontains__in=keywords)
        # keyword_posts = Post.objects.filter(keywords__icontains__in=flattened_keywords)


        return posts

    class Meta:
        db_table = 'post'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=1000)
    commenting_date = models.DateTimeField(auto_now_add=True)
    objects = Comment_Manage()

    class Meta:
        db_table = 'comment'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liking_date = models.DateTimeField(auto_now_add=True)
    objects = Like_Manage()

    class Meta:
        db_table = 'like'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorite'
        unique_together = ['user', 'post']
