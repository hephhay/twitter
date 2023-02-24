from django.test import TestCase

from utils.models import BaseModel
from post.models import Tweet

class TestBaseModel(TestCase):

    fixtures = ['test_data.json']

    def setUp(self) -> None:
        super().setUp()
        self.model = Tweet

    def test_base_model_ordering(self):
        self.assertTrue(issubclass(self.model, BaseModel))
        result = list(self.model.objects.all()[:5])

        self.assertListEqual(
            result,
            sorted(result,key = lambda tweet: tweet.created_at, reverse=True)
        )

        self.assertListEqual(
            result,
            sorted(result,key = lambda tweet: tweet.updated_at, reverse=True)
        )