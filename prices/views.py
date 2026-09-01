from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from contact.models import ContactAddress
from prices.serializers import ContactAddressSerializer
from vcelnice.serializers import PriceSerializer
from .models import Price


@api_view(["GET"])
def location_list(request):
    if request.method == "GET":
        locations = ContactAddress.objects.all()
        serializer = ContactAddressSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)
