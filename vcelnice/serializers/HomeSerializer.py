from rest_framework import serializers
from home.models import Home


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ('id', 'title', 'text', 'icon')
