from rest_framework import serializers

from video.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "caption",
            "description",
            "file",
            "thumb",
            "created",
            "updated",
            "youtube_id",
        )
