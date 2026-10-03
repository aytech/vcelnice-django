from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Recipe
from .serializers import RecipeSerializer


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

class RecipeAPIRootView(PublicReadOnlyAPIView):
    @staticmethod
    def get(request):
        return Response({
            "photos": reverse(
                "recipe-api:recipe-list",
                request=request,
            ),
        })

class RecipeAPIListView(PublicReadOnlyAPIView):
    @staticmethod
    def get(_):
        recipes = Recipe.objects.order_by("-updated").all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response({"recipes": serializer.data})

