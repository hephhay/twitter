from typing import Any

from django.shortcuts import get_object_or_404
from django.db.models import Count, OuterRef, Subquery

from rest_framework.response import Response

class ViewSetMixins:

    def generic_list(self: Any, queryset) -> Any:
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_by_id(self: Any) -> Any:
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        return get_object_or_404(
            self.get_queryset(),
            **filter_kwargs
        )

    def count_subquery(self: Any, related_field: str):
        return Subquery(self.model.objects\
                .filter(**{related_field : OuterRef('pk')})\
                    .values(related_field)\
                        .annotate(count = Count('pk'))\
                            .values('count')
        )