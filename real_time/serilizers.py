from rest_framework import serializers
from post.serializers import TweetSerilizer

from real_time.models import Group, Message,  Notification
from utils.const import READ_ONLY_FIELDS
from users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        exclude = ('participants',)
        read_only_fields = READ_ONLY_FIELDS

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        exclude = ('seen_by',)
        read_only_fields = READ_ONLY_FIELDS

class NotificationSerializer(serializers.ModelSerializer):
    tweet = TweetSerilizer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = READ_ONLY_FIELDS