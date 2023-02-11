from rest_framework import serializers, viewsets
from django.core.files.uploadedfile import UploadedFile

from post.models import Tweet, TweetMedia
from utils.helpers import validate_image
from utils.const import READ_ONLY_FIELDS
from utils.serializers import RecursiveSingleField


class TweetMediaSerilizer(serializers.ModelSerializer):
    def validate_file(self, image: UploadedFile):
        validate_image(image)

    class Meta:
        model = TweetMedia
        fields = '__all__'
        read_only_feilds = ['id', 'created_at']

class TweetSerilizer(serializers.ModelSerializer):

    num_reply = serializers.IntegerField(read_only = True)

    num_retweet = serializers.IntegerField(read_only = True)

    num_likes = serializers.IntegerField(read_only = True)

    reply = RecursiveSingleField(required = False, read_only = True)

    retweet = RecursiveSingleField(required = False, read_only = True)

    media = TweetMediaSerilizer(
        source = 'tweet_media',
        read_only = True,
        many =True
    )

    def create(self, validated_data):
        context = self.context
        view: viewsets.ModelViewSet  = context.get('view', None)
        action = view.action

        if action == 'reply_tweet':
            validated_data['reply_to_id'] = view.kwargs.get('pk', None)

        elif action == 'retweet':
            validated_data['tweet_id'] = view.kwargs.get('pk', None)

        validated_data['created_by'] = context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Tweet
        exclude = ('likes',)
        read_only_fields = ('tags', *READ_ONLY_FIELDS)
