# Generated by Django 4.1.2 on 2022-10-30 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_tweet_options_rename_reply_tweet_reply_to_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReTweet',
        ),
    ]