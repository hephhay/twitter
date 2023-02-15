from unittest import TestCase, mock

from django.db.models import QuerySet
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from utils.filters import CustomFilter
from utils.models import BaseModel

class CustomFilterTest(TestCase):

    def setUp(self):
        super().setUp()
        self.filter = CustomFilter
        self.model = mock.MagicMock(spec = BaseModel)
        self.before = timezone.now()
        self.after = self.before - relativedelta(years=2)

    def get_queryset(self):
        mock_qs = mock.MagicMock(spec = QuerySet)
        mock_qs.model = self.model
        mock_qs.all.return_value = mock_qs
        mock_qs.filter.return_value = mock_qs
        return mock_qs

    def test_created_at(self):
        mock_queryset = self.get_queryset()
        
        mock_filter = CustomFilter(
            data = {
                'created_at_before': self.before,
                'created_at_after': self.after
                },
            queryset= mock_queryset
        )

        self.assertEqual(
            mock_filter.qs.filter.call_args,
            mock.call(created_at__range = (self.after, self.before))
        )

    def test_updated_at(self):
        mock_queryset = self.get_queryset()
        
        mock_filter = CustomFilter(
            data = {
                'updated_at_before': self.before,
            },
            queryset= mock_queryset
        )

        self.assertEqual(
            mock_filter.qs.filter.call_args,
            mock.call(updated_at__lte = self.before)
        )