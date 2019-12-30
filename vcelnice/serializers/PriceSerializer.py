from rest_framework import serializers
from prices.models import Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ("id", "title", "price", "weight", "in_store", "amount_description", "image")
