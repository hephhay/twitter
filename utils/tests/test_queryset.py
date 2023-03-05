from django.test import TestCase

from users.models import User
from post.models import Tweet

class CustomQuerySetTestCase(TestCase):
    fixtures = ['test_data.json']

    def test_num_many_to_many(self):
        result = User.objects.all()\
            .num_many_to_many('followers').get(username = 'hephhay')
        self.assertEqual(1, result.num_followers)

    def test_num_one_to_many(self):
        tweet1, tweet2 = Tweet.objects.all()\
            .num_one_to_many('replies', 'retweets')[:2]
        self.assertEqual(1, tweet1.num_replies)
        self.assertEqual(1, tweet2.num_retweets)
