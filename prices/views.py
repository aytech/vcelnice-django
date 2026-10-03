from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from contact.models import ContactAddress
from .serializers import PricesSerializer
from .models import Price


# @api_view(["GET"])
# def location_list(request):
#     if request.method == "GET":
#         locations = ContactAddress.objects.all()
#         serializer = ContactAddressSerializer(locations, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(None, status=status.HTTP_400_BAD_REQUEST)

class PublicReadOnlyAPIView(APIView):
    """
    Base class for endpoints that intentionally expose public read-only data.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    http_method_names = ["get", "head", "options"]

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        # Availability can change through Django Admin, so browsers
        # and proxies should not retain a stale response
        response["Cache-Control"] = "no-store"
        return response

class PricesAPIRootView(PublicReadOnlyAPIView):
    @staticmethod
    def get(request):
        return Response({
            "prices": reverse(
                "prices-api:prices-list",
                request=request,
            )
        })

class PricesAPIListView(PublicReadOnlyAPIView):
    @staticmethod
    def get(_):
        prices = Price.objects.all()
        serializer = PricesSerializer(prices, many=True)
        return Response({"prices": serializer.data})
