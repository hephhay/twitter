from typing import Any

from django.db.models import Count, OuterRef, Exists

from rest_framework import (
    viewsets,
    serializers,
    permissions,
    status,
    exceptions,
    mixins
)
from rest_framework.decorators import action
from rest_framework.response import Response

from djoser.conf import settings

from users.filters import UserFilter
from users.models import User
from users.serializers import UserSerializer
from twitter.mixins import ViewSetMixins

class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    ViewSetMixins
):
    queryset = User.objects.all().prefetch_related('followers')

    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    lookup_field = settings.USER_ID_FIELD

    filterset_class = UserFilter

    search_fields = [
        'id',
        'email',
        'first_name',
        'last_name',
        'location'
    ]

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()

        if self.request.method == 'GET':
            queryset = queryset.annotate_nums()

            queryset = self.checkFollows(queryset)\
                    .order_by('-num_followers')

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

        if user.followers.count() >= 10 and (not user.is_verified):
            user.is_verified = True

        user.save()

        return Response({"message" : "success"}, status = status.HTTP_200_OK)

    def list_view(self, queryset) -> Any:
        queryset = self.checkFollows(queryset).order_by(
            'follow__start_follow'
        )

        return self.generic_list(queryset)

    @action(
        detail=True,
        methods=['get'],
    )
    def followers(self, request, *args, **kwargs):
        queryset = self.get_by_id().followers.all()

        return self.list_view(queryset)

    @action(
        detail=True,
        methods=['get'],
    )
    def following(self, request, *args, **kwargs):
        queryset = queryset = self.get_by_id().following.all()

        return self.list_view(queryset)