from rest_framework import serializers
from documents.models import Document


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('description', 'file', 'type')
