from rest_framework import serializers

from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "thumb",
            "preview",
            "text",
            "created",
            "updated"
        ]
        read_only_fields = fields