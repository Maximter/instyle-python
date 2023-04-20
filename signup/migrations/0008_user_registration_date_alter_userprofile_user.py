# Generated by Django 4.1.7 on 2023-04-20 09:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0007_remove_user_avatar_remove_user_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='registration_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='signup.user'),
        ),
    ]
