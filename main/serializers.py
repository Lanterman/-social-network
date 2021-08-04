from rest_framework.serializers import ModelSerializer

from main.models import Published


class UserPublishedSerializer(ModelSerializer):
    class Meta:
        model = Published
        fields = ('published', 'like', 'in_mark', 'rate')
