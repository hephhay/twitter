# Generated by Django 4.1.2 on 2022-10-30 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0011_alter_tweet_reply_to_alter_tweet_tweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
