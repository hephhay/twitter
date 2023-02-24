from django.test import TestCase
from django.http import QueryDict

from rest_framework.test import APIRequestFactory

from users.models import User
from utils.pagination import CustomPageNumberPagination

class TestCustomPageNumberPagination(TestCase):
    fixtures = ['test_data.json']

    def setUp(self) -> None:
        super().setUp()
        self.model = User
        self.pagination = CustomPageNumberPagination()
        self.factory = APIRequestFactory()

    def test_pagination_properties(self):
        self.assertEqual(self.pagination.page_size, 5)
        self.assertEqual(self.pagination.max_page_size, 100)
        self.assertEqual(self.pagination.page_size_query_param, 'page_size')

    def test_pagination_results(self):
        queryset = self.model.objects.all()
        request = self.factory.get('/users/')
        request.query_params = QueryDict(request.GET.urlencode()) # type: ignore
        paginated_queryset = self.pagination\
            .paginate_queryset(queryset=queryset, request=request)

        self.assertIsNotNone(paginated_queryset)
        if paginated_queryset:
            self.assertEqual(len(paginated_queryset), 5)

    def test_custom_page_size(self):
        request = self.factory.get('users/', {'page_size': 2})
        request.query_params = QueryDict(request.GET.urlencode()) # type: ignore
        queryset = self.model.objects.all()
        paginated_queryset = self.pagination.\
            paginate_queryset(queryset, request)

        self.assertIsNotNone(paginated_queryset)
        if paginated_queryset:
            self.assertEqual(len(paginated_queryset), 2)

    def test_max_page_size(self):
        request = self.factory.get('users/', {'page_size': 7})
        request.query_params = QueryDict(request.GET.urlencode()) # type: ignore
        queryset = self.model.objects.all()
        self.pagination.max_page_size = 6
        paginated_queryset = self.pagination.\
            paginate_queryset(queryset, request)

        self.assertIsNotNone(paginated_queryset)
        if paginated_queryset:
            self.assertEqual(len(paginated_queryset), 6)
