from typing import Any

from rest_framework import (
    viewsets,
    status,
    permissions,
    mixins
)
from rest_framework.decorators import action
from rest_framework.response import Response

from post.models import Tweet, TweetMedia
from post.serializers import TweetMediaSerilizer, TweetSerilizer
from post.filters import TweetFilter
from utils.helpers import cast_user
from users.serializers import UserSerializer
from users.views import UserViewSet
from utils.permissions import OwnerOrAdminOrReadOnly
from utils.mixins import ViewSetMixins
from utils.serializers import GeneralSerializer

class TweetViewSet(viewsets.ModelViewSet, ViewSetMixins):
    queryset = Tweet.objects.all()

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

        if self.action in ['replies', 'likes', 'retweets']:
            queryset = self.get_by_id(queryset)
            
        if self.action == 'likes':
            user =  cast_user(self.request.user)
            return queryset.likes.all().follow_count()\
                .check_follow(user.id)\
                    .order_by('-like__liked_on')


        if self.request.method == 'GET':
            return queryset.prefetch_related(
                'retweet',
                'reply',
                'tweet_media'
            ).prop_count().order_by('num_likes')

        return queryset

    def list(self, request, *args, **kwargs):
        return self.generic_list(self.get_queryset())

    @action(
        detail=True,
        methods=['post', 'delete'],
        serializer_class = GeneralSerializer,
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
        filterset_class = UserViewSet.filterset_class,
        search_fields = UserViewSet.search_fields,
    )
    def likes(self, request, *args, **kwargs):
        return self.generic_list(self.get_queryset())

    @action(
        detail=True,
        methods=['get']
    )
    def replies(self, request, *args, **kwargs):
        queryset = self.get_queryset().replies.all().prop_count()\
            .order_by('-created_at')

        return self.generic_list(queryset)

    @action(
        detail=True,
        methods=['get']
    )
    def retweets(self, request, *args, **kwargs):
        queryset = self.get_queryset().retweets.all().prop_count()\
            .order_by('-created_at')

        return self.generic_list(queryset)


class TweetMediaViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    ViewSetMixins
):
    queryset = TweetMedia.objects.all().prefetch_related('tweet')

    serializer_class = TweetMediaSerilizer

    permission_classes = [OwnerOrAdminOrReadOnly]

    lookup_field = 'file'

    owner_field = 'tweet__created_by'
