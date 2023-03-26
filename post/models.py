from datetime import date
import datetime
from django.db import models
from django.utils import timezone

from signup.models import User

# Create your models here.
class PostManager(models.Manager):
    def create_post(self, id_post, user, comment):
        post = self.create(id_post=id_post, user=user, comment=comment)
        return post

# Create your models here. 
class Post(models.Model,):
    id_post = models.CharField(unique=True, max_length=13)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )
    date_post = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=1500)
    objects = PostManager()
    
    class Meta:
        db_table = 'post'
