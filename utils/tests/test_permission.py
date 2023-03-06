from django.test import TestCase, Client
from rest_framework import status

from users.models import User

class TestCurrentUserOrAdminOrReadOnly(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username = 'titi_adewale')
        self.admin = User.objects.get(username = 'hephhay')

    def test_user_can_view_own_object(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/auth/users/{self.user.username}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_modify_own_objects(self):
        self.client.force_login(self.user)
        response = self.client.patch(f'/auth/users/{self.user.username}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_modify_other_objects(self):
        other_user = User.objects.get(username='tobias')
        self.client.force_login(self.user)
        response = self.client.patch(f'/auth/users/{other_user.username}/', {'username': 'toba'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_modify_all_objects(self):
        other_user = User.objects.get(username='tobias')
        self.client.force_login(self.admin)
        response = self.client.patch(f'/auth/users/{other_user.username}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
