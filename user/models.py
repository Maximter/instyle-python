from django.db import models
from signup.models import User


class FollowManager(models.Manager):
    def create_post(self, follower, following):
        post = self.create(follower=follower, following=following,)
        return post


class Follow(models.Model,):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    objects = FollowManager()

    class Meta:
        db_table = 'follow'


class CloseFriend(models.Model):
    user = models.ForeignKey(User, related_name='user_close_friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_close_friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'close_friend'
        unique_together = ['user', 'friend']


class Blacklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')

    class Meta:
        db_table = 'black_list'
        unique_together = ['user', 'blocked_user']