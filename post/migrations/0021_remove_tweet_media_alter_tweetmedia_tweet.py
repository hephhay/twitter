# Generated by Django 4.1.2 on 2023-02-11 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0020_tweetmedia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='media',
        ),
        migrations.AlterField(
            model_name='tweetmedia',
            name='tweet',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='tweet_media', to='post.tweet'),
        ),
    ]