from rest_framework import serializers

from .models import Price


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            "id",
            "title",
            "price",
            "weight",
            "in_store",
            "amount_description",
            "image"
        )
        read_only_fields = fields