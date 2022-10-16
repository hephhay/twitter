# Generated by Django 4.1.2 on 2022-10-16 19:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='likes',
            field=models.ManyToManyField(related_name='%(class)s_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='likes',
            field=models.ManyToManyField(related_name='%(class)s_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
