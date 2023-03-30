# Generated by Django 4.1.7 on 2023-03-25 16:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('signup', '0005_alter_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_post', models.CharField(max_length=13, unique=True)),
                ('date_post', models.DateField(default=datetime.date.today)),
                ('comment', models.CharField(max_length=1500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='signup.user')),
            ],
            options={
                'db_table': 'post',
            },
        ),
    ]