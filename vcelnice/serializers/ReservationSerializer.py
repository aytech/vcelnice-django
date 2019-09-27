from rest_framework import serializers
from prices.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('amount', 'email', 'message', 'title', 'location')
