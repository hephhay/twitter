from unittest import TestCase, mock

from utils.managers import CustomManager
from utils.queryset import CustomQuerySet

class CustommangerTest(TestCase):

    def setUp(self):
        super().setUp()
        self.manager = CustomManager()

    def test_all_is_instance_qs(self):
        self.assertIsInstance(self.manager.get_queryset(), CustomQuerySet)
