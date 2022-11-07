from typing import Any

from django.db import models

class CustomQuerySet(models.QuerySet): #type: ignore
    def num_many_to_many(self, *args: str) -> Any:
        for relation in args:
            self = self.annotate(**{f'num_{relation}' : models.Count(relation)})

        return self

    def num_one_to_many(self: Any, *args: str):
        for related_field in args:
            self = self.annotate(**{f'num_{related_field}' : models.Subquery(self.model.objects\
                .filter(**{related_field : models.OuterRef('pk')})\
                    .values(related_field)\
                        .annotate(count = models.Count('pk'))\
                            .values('count')
            )})

        return self