from django.db import models

# Create your models here.
class User(models.Model,):
    email = models.CharField(unique=True, max_length=45)
    name_lastname = models.CharField(max_length=40)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=65)
    bio = models.CharField(max_length=300, default='')
    avatar = models.BooleanField(default=False)
    verificated = models.BooleanField(default=False)
    online = models.CharField(default='1', max_length=10)
    class Meta:
        db_table = 'user'
