# Generated by Django 4.1.7 on 2023-03-24 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0004_alter_token_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=105),
        ),
    ]
