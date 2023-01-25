from rest_framework import serializers

class RecursiveSingleField(serializers.Serializer):
    def to_representation(self, value):
        serializer: serializers.Serializer = self.parent\
            .__class__(value, context=self.context)  # type: ignore
        return serializer.data
