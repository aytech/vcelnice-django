from rest_framework import serializers

from .models import Article


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "text",
            "icon",
            "created",
            "updated"
        ]
        read_only_fields = fields