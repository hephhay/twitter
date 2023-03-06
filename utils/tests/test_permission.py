from typing import cast, Dict

from django.http import HttpResponse
from django.test import TestCase, Client

from rest_framework import status
from rest_framework.response import Response

from users.models import User
from post.models import Tweet

class TestCurrentUserOrAdminOrReadOnly(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username = 'titi_adewale')
        self.other_user = User.objects.get(username='tobias')
        self.admin = User.objects.get(username = 'hephhay')
        self.content_type = 'application/json'
        self.response = None

    def assert_data(self, key: str, value: str):
        json_response = cast(Response, self.response)
        data = cast(Dict[str, str], json_response.data)
        self.assertEqual(data.get(key, None), value)

    def anon_user_can_view_own_object(self):
        self.response = self.client.get(f'/auth/users/{self.user.username}/')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_user_can_modify_own_objects(self):
        self.client.force_login(self.user)
        self.response = self.client.patch(
            f'/auth/users/{self.user.username}/',
            {'username': 'titlayo'},
            content_type=self.content_type
        )
        self.assert_data('username', 'titlayo')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_user_cannot_modify_other_objects(self):
        self.client.force_login(self.user)
        self.response = self.client.patch(
            f'/auth/users/{self.other_user.username}/',
            {'username': 'toba'}
        )
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_modify_all_objects(self):
        self.client.force_login(self.admin)
        self.response = self.client.patch(
            f'/auth/users/{self.other_user.username}/',
            {'username': 'toba'},
            content_type=self.content_type
        )
        self.assert_data('username', 'toba')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class OwnerOrAdminOrReadOnlyTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username = 'titi_adewale')
        self.other_user = User.objects.get(username='tobias')
        self.admin = User.objects.get(username = 'hephhay')
        self.owned = Tweet.objects.filter(created_by = self.user)[0]
        self.content_type = 'application/json'
        self.response = None

    def assert_data(self, key: str, value: str):
        json_response = cast(Response, self.response)
        data = cast(Dict[str, str], json_response.data)
        self.assertEqual(data.get(key, None), value)

    def anon_user_can_view_own_object(self):
        self.client.force_login(self.other_user)
        self.response = self.client.get(f'/tweet/{self.owned.id}/')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_user_cannot_modify_other_objects(self):
        self.client.force_login(self.other_user)
        self.response = self.client.patch(
            f'/tweet/{self.owned.id}/',
            {'content': 'Hello Testing'}
        )
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_modify_own_object(self):
        self.client.force_login(self.user)
        self.response = self.client.patch(
            f'/tweet/{self.owned.id}/',
            {'content': 'Hello Testing'},
            content_type=self.content_type
        )
        self.assert_data('content', 'Hello Testing')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_admin_can_modify_all_objects(self):
        self.client.force_login(self.admin)
        self.response = self.client.patch(
            f'/tweet/{self.owned.id}/',
            {'content': 'Hello Testing'},
            content_type=self.content_type
        )
        self.assert_data('content', 'Hello Testing')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
