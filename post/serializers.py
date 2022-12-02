from rest_framework import serializers, viewsets

from post.models import Tweet
from twitter.const import READ_ONLY_FIELDS
from twitter.serializers import RecursiveSingleField

class TweetSerilizer(serializers.ModelSerializer):

    num_reply = serializers.IntegerField(read_only = True)

    num_retweet = serializers.IntegerField(read_only = True)

    num_likes = serializers.IntegerField(read_only = True)

    reply = RecursiveSingleField(required=False, read_only = True)

    retweet = RecursiveSingleField(required=False, read_only = True)

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
        read_only_fields = ('likes','tags', *READ_ONLY_FIELDS)