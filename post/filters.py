from django_filters import BooleanFilter, CharFilter

from post.models import Tweet
from utils.filters import CustomFilter

class TweetFilter(CustomFilter):
    rem_reply = BooleanFilter(field_name='reply', lookup_expr='isnull')
    rem_retweet = BooleanFilter(field_name='retweet', lookup_expr='isnull')
    created_by = CharFilter()
    content = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Tweet
        fields = [
            'created_by',
            'content',
            'created_at',
            'updated_at'
        ]