from django.contrib import admin

from post.models import Tweet, ReTweet

# Register your models here.

admin.register(Tweet)
admin.register(ReTweet)