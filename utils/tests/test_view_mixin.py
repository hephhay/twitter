from collections import OrderedDict
from typing import cast, Any

from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

from rest_framework.test import APIRequestFactory


from users.models import User
from users.serializers import UserSerializer
from utils.mixins import ViewSetMixins


class TestViewSetMixins(TestCase):

    fixtures = ['test_data.json']

    def setUp(self):
        super().setUp()
        self.view_class = ViewSetMixins
        self.view_class.queryset = User.objects.all()
        self.view_class.serializer_class = UserSerializer # type: ignore
        
        # self.view = self.view_class.as_view()
        self.request = APIRequestFactory()

    def test_generic_list(self):
        req = self.request.get('/')
        req.query_params = req.GET # type: ignore
        req.user = AnonymousUser()

        req_view = self.view_class()
        req_view.setup(request=req)
        req_view.initial(request=req)
        res = req_view.generic_list(self.view_class.queryset)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, dict)

        res.data = cast('OrderedDict[str, Any]', res.data)

        res_keys = {'count', 'next', 'previous', 'results'}
        self.assertTrue(
            res_keys.issubset(set(res.data.keys()))
        )
        self.assertIsInstance(res.data.get('results', None), list)

        # print(set(res.data.keys()) == {'count', 'next', 'previous', 'results'})
