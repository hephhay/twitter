# Generated by Django 4.1.2 on 2022-10-25 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_rename_tweet_tweet_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retweet',
            name='tweet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_tweet', to='post.tweet'),
        ),
    ]