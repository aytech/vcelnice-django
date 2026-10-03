from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Home
from .seralizers import HomeSerializer


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


class HomeAPIRootView(PublicReadOnlyAPIView):
    """
    Return the single public home resource.
    """
    def get(self, _):
        home = Home.objects.filter(
            pk=Home.SINGLETON_PK,
        ).first()

        if home is None:
            home = Home()

        serializer = HomeSerializer(home)

        return Response(serializer.data)