from django_filters import FilterSet, DateTimeFromToRangeFilter

from utils.models import BaseModel

class CustomFilter(FilterSet):
    created_at = DateTimeFromToRangeFilter()
    updated_at = DateTimeFromToRangeFilter()
