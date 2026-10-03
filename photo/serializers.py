from rest_framework import serializers

from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [
            "id",
            "caption",
            "image",
            "thumb",
            "width",
            "height",
            "created"
        ]
        read_only_fields = fields