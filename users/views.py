from typing import Any

from django.db.models import Count, OuterRef, Exists

from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework import permissions, status, exceptions, mixins
from rest_framework.response import Response

from djoser.conf import settings

from users.models import User
from users.serializers import UserSerializer

class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = settings.USER_ID_FIELD
    search_fields = [
        'id',
        'email',
        'first_name',
        'last_name',
        'location'
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ('retrieve', 'list'):
            queryset = queryset.annotate(
                num_followers = Count('followers'),
                num_following = Count('following'),
            ).order_by('-created_at')

            queryset = self.checkFollows(queryset)

        return queryset

    def checkFollows(self, queryset) -> Any:
        UserModel : Any = User

        return queryset.annotate(
            follows_you = Exists(
                UserModel.following.through.objects.filter(
                    user_id = self.request.user.id,
                    follower_id = OuterRef('pk')
                )
            )
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        serializer_class = serializers.Serializer
    )
    def follow(self, request, *args, **kwargs):
        user: User = self.get_object()
        auth_user: User = request.user

        if user.id == auth_user.id:
            raise exceptions.ParseError("you cannot follow yourself")

        if request.method == 'POST':
            user.followers.add(request.user.id)
        else:
            user.followers.remove(request.user.id)

        if user.followers.count() > 10:
            user.is_verified = True
        else:
            user.is_verified = False

        user.save()

        return Response({"message" : "success"}, status = status.HTTP_200_OK)

    def list_view(self, queryset) -> Any:
        queryset = self.checkFollows(queryset).order_by(
            'follow__start_follow'
        )
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['get'],
    )
    def followers(self, request, *args, **kwargs):
        queryset = self.get_object().followers.all()
        return self.list_view(queryset)

    @action(
        detail=True,
        methods=['get'],
    )
    def following(self, request, *args, **kwargs):
        queryset = self.get_object().following.all()
        return self.list_view(queryset)