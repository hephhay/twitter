from rest_framework.serializers import Serializer, CharField

class GeneralSerializer(Serializer):
    message = CharField(read_only = True)

    class Meta:
        fields = '__all__'
