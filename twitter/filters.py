from django_filters import FilterSet, DateFromToRangeFilter

class CustomFilter(FilterSet):
    created_at = DateFromToRangeFilter()
    updated_at = DateFromToRangeFilter()