# Generated by Django 4.1.7 on 2023-06-15 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0017_userprofile_message_visibility_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='message_visibility',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_visibility',
        ),
        migrations.AddField(
            model_name='user',
            name='message_visibility',
            field=models.CharField(default='all', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_visibility',
            field=models.CharField(default='all', max_length=30),
        ),
    ]
