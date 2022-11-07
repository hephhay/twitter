from rest_framework import serializers

from post.models import Tweet
from twitter.const import READ_ONLY_FIELDS

class TweetSerilizer(serializers.ModelSerializer):

    num_reply = serializers.IntegerField(read_only = True)

    num_retweet = serializers.IntegerField(read_only = True)

    num_likes = serializers.IntegerField(read_only = True)

    class Meta:
        model = Tweet
        exclude = ['likes']
        read_only_fields = READ_ONLY_FIELDS + ('likes','tags')

    def create(self, validated_data):
        context = self.context
        view = context.get('view', None)
        action = view.action

        if action == 'reply_tweet':
            validated_data['reply_to_id'] = view.kwargs.get('pk', None)

        elif action == 'retweet':
            validated_data['tweet_id'] = view.kwargs.get('pk', None)

        validated_data['created_by'] = context['request'].user
        return super().create(validated_data)