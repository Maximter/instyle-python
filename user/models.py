from django.db import models

from signup.models import User

# Create your models here.

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

