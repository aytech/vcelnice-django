from rest_framework import serializers

from video.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "caption",
            "description",
            "thumb",
            "created",
            "updated",
            "youtube_id",
        )
