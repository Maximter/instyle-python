import uuid
from django.db import models

class UserManager(models.Manager):
    def create_user(self, email, name_lastname, username, password):
        user = self.create(email=email, name_lastname=name_lastname, username=username, password=password)
        return user

class TokenManager(models.Manager):
    def create_token(self, user):
        token = self.create(user=user)
        return token
    

# Create your models here. 
class User(models.Model,):
    email = models.CharField(unique=True, max_length=45)
    name_lastname = models.CharField(max_length=40)
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=105)
    bio = models.CharField(max_length=300, default='')
    avatar = models.BooleanField(default=False)
    verificated = models.BooleanField(default=False)
    online = models.CharField(default='1', max_length=10)
    objects = UserManager()
    
    class Meta:
        db_table = 'user'


class Token(models.Model,):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    objects = TokenManager()
    
    class Meta:
        db_table = 'token'