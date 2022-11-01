from typing import Any

from django.db.models import Count

from rest_framework import viewsets, serializers, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


from post.models import Tweet
from post.serializers import TweetSerilizer
from users.serializers import UserSerializer
from twitter.permissions import OwnerOrAdminOrReadOnly
from twitter.mixins import ViewSetMixins

class TweetViewSet(viewsets.ModelViewSet, ViewSetMixins):
    queryset = Tweet.objects.all()

    serializer_class = TweetSerilizer

    permission_classes = [OwnerOrAdminOrReadOnly]

    owener_field = 'owner_field'

    model = Tweet

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()

        if self.request.method == 'GET':
            queryset = queryset.annotate(
                num_replies = self.count_subquery('reply_to'),
                num_retweet = self.count_subquery('tweet'),
                num_likes = Count('likes')
            ).order_by('created_at')

        return queryset


    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset().filter(
            tweet = None,
            reply_to = None
        )

        return self.generic_list(queryset)

    @action(
        detail=True,
        methods=['post', 'delete'],
        serializer_class = serializers.Serializer,
        permission_classes = [permissions.IsAuthenticated]
    )
    def like_tweet(self, request, *args, **kwargs):
        tweet: Tweet = self.get_object()

        if request.method == 'POST':
            tweet.likes.add(request.user)

        else:
            tweet.likes.remove(request.user)

        return Response({"message" : "success"}, status = status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
    )
    def reply_tweet(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(
        detail=True,
        methods=['post'],
    )
    def retweet(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(
        detail=True,
        methods=['get'],
        serializer_class = UserSerializer,
    )
    def likes(self, request, *args, **kwargs):
        queryset = self.get_by_id().likes.all()\
            .annotate_nums().order_by('like__liked_on')

        return self.generic_list(queryset)