from rest_framework import serializers
from photo.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'caption', 'image', 'thumb', 'width', 'height', 'created')
