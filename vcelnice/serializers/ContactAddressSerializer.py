from rest_framework import serializers
from contact.models import ContactAddress


class ContactAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactAddress
        fields = ('address',)
