from django.contrib import admin

from real_time.models import Group, Message, Notification

# Register your models here.

admin.register(Group)
admin.register(Message)
admin.register(Notification)
