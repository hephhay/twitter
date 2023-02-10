from typing import Any, Callable, cast

from rest_framework.serializers import Serializer

SerialFunc = Callable[[Any, Any], Serializer]

class RecursiveSingleField(Serializer):
    def to_representation(self, value: Any):
        intermediate = cast(SerialFunc, self.parent.__class__)
        serializer = intermediate(value, context=self.context) #type: ignore
        return serializer.data
