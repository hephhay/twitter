from typing import Any

from rest_framework import viewsets, serializers, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from post.models import Tweet
from post.serializers import TweetSerilizer
from post.filters import TweetFilter
from twitter.util import cast_user
from users.serializers import UserSerializer
from twitter.permissions import OwnerOrAdminOrReadOnly
from twitter.mixins import ViewSetMixins

class TweetViewSet(viewsets.ModelViewSet, ViewSetMixins):
    queryset = Tweet.objects.prefetch_related('retweet', 'reply')

    serializer_class = TweetSerilizer

    permission_classes = [OwnerOrAdminOrReadOnly]

    filterset_class = TweetFilter

    search_fields = [
        'created_by__email',
        'created_by__first_name',
        'created_by__last_name',
        'created_by__location',
        'created_by__username'
        'content',
        'id',
        'tags'
    ]

    owner_field = 'created_by'

    model = Tweet

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()

        if self.action == 'retrieve':
            queryset = queryset
            print(queryset.model)

        if self.request.method == 'GET':
            queryset = queryset.prop_count().order_by('num_likes')

        return queryset


    def list(self, request, *args, **kwargs):
        return self.generic_list(self.get_queryset())

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
        user =  cast_user(self.request.user)
        queryset = self.get_by_id().likes.all().follow_count()\
            .check_follow(user.id)\
                .order_by('-like__liked_on')

        return self.generic_list(queryset)

    @action(
        detail=True,
        methods=['get']
    )
    def replies(self, request, *args, **kwargs):
        queryset = self.get_by_id().replies.all().prop_count()\
            .order_by('-created_at')

    @action(
        detail=True,
        methods=['get']
    )
    def retweets(self, request, *args, **kwargs):
        queryset = self.get_by_id().retweets.all().prop_count()\
            .order_by('-created_at')

        return self.generic_list(queryset)
