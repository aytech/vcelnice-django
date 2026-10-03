from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Video
from .serializers import VideoSerializer

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

class VideoAPIRootView(PublicReadOnlyAPIView):
    @staticmethod
    def get(request):
        return Response({
            "videos": reverse(
                "video-api:video-list",
                request=request,
            ),
        })

class VideoAPIListView(PublicReadOnlyAPIView):
    @staticmethod
    def get(_):
        videos = Video.objects.exclude(youtube_id__isnull=True).exclude(
            youtube_id=""
        ).order_by("-updated")
        serializer = VideoSerializer(videos, many=True)
        return Response({"videos": serializer.data})