from django.contrib import admin

from users.models import User, Bookmark, Notification

# Register your models here.

admin.register(User)
admin.register(Bookmark)
admin.register(Notification)