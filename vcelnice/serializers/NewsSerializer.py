from rest_framework import serializers
from news.models import Article


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'icon', 'created', 'updated')
