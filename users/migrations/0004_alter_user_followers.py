# Generated by Django 4.1.2 on 2022-10-27 19:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
