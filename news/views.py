from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .serializers import NewsSerializer
from .models import Article


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

class NewsAPIRootView(PublicReadOnlyAPIView):
    @staticmethod
    def get(request):
        return Response({
            "news": reverse(
                "news-api:news-list",
                request=request,
            ),
        })

class NewsAPIListView(PublicReadOnlyAPIView):
    @staticmethod
    def get(_):
        news = Article.objects.order_by("-updated").all()
        serializer = NewsSerializer(news, many=True)
        return Response({"news": serializer.data})