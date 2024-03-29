# Generated by Django 4.1.7 on 2023-03-27 16:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0005_alter_user_password'),
        ('post', '0007_alter_post_date_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('comment', models.CharField(default='', max_length=1500)),
                ('date_comment', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.user')),
            ],
            options={
                'db_table': 'post_interaction',
            },
        ),
    ]
