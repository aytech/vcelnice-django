from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from documents.models import Document
from news.models import Article
from photo.models import Photo
from recipe.models import Recipe

from vcelnice.serializers import (
    CertificateSerializer,
    NewsSerializer,
    PhotoSerializer,
    RecipeSerializer,
    VideoSerializer,
)
from video.models import Video


@api_view(["GET"])
def news_list(request):
    if request.method == "GET":
        news = Article.objects.order_by("-updated").all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def photo_list(request):
    if request.method == "GET":
        news = Photo.objects.order_by("-created").all()
        serializer = PhotoSerializer(news, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def recipe_list(request):
    if request.method == "GET":
        recipes = Recipe.objects.order_by("-updated").all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def certificate_list(request):
    if request.method == "GET":
        certificates = Document.objects.all()
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def video_list(request):
    if request.method == "GET":
        videos = Video.objects.exclude(youtube_id__isnull=True).exclude(
            youtube_id=""
        ).order_by("-updated")
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def csrf_token(request):
    if request.method == "GET":
        return Response(get_token(request))
    return Response(None, status=status.HTTP_400_BAD_REQUEST)
