from django.middleware.csrf import get_token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from contact.models import ContactAddress
from home.models import Home
from news.models import Article
from photo.models import Photo
from prices.models import Price
from recipe.models import Recipe
from documents.models import Document
from vcelnice.serializers.ContactAddressSerializer import ContactAddressSerializer
from vcelnice.serializers.ContactSerializer import ContactSerializer
from vcelnice.settings import YOUTUBE_STATUS_PENDING_UPLOAD
from video.models import Video
from vcelnice.serializers.HomeSerializer import HomeSerializer
from vcelnice.serializers.NewsSerializer import NewsSerializer
from vcelnice.serializers.PhotoSerializer import PhotoSerializer
from vcelnice.serializers.PriceSerializer import PriceSerializer
from vcelnice.serializers.RecipeSerializer import RecipeSerializer
from vcelnice.serializers.ReservationSerializer import ReservationSerializer
from vcelnice.serializers.CertificateSerializer import CertificateSerializer
from vcelnice.serializers.VideoSerializer import VideoSerializer


@api_view(['GET'])
def home_text(request):
    default_response = Response(HomeSerializer(Home(), many=False).data)
    if request.method != 'GET':
        return default_response
    try:
        text = Home.objects.get()
        serializer = HomeSerializer(text, many=False)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return default_response


@api_view(['GET'])
def news_list(request):
    if request.method == 'GET':
        news = Article.objects.order_by('-updated').all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def photo_list(request):
    if request.method == 'GET':
        news = Photo.objects.order_by('-created').all()
        serializer = PhotoSerializer(news, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def prices_list(request):
    if request.method == 'GET':
        news = Price.objects.all()
        serializer = PriceSerializer(news, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def location_list(request):
    if request.method == 'GET':
        locations = ContactAddress.objects.all()
        serializer = ContactAddressSerializer(locations, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def recipe_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.order_by('-updated').all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def certificate_list(request):
    if request.method == 'GET':
        certificates = Document.objects.all()
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def video_list(request):
    if request.method == 'GET':
        videos = Video.objects.filter(youtube_status__gt=YOUTUBE_STATUS_PENDING_UPLOAD).order_by('-updated').all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def csrf_token(request):
    if request.method == 'GET':
        return Response(get_token(request))
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reserve(request):
    if request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def contact(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)
