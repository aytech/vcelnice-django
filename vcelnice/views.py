from django.core.exceptions import ObjectDoesNotExist
from django.middleware.csrf import get_token
from django.utils.translation import activate, ugettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from documents.models import Document
from home.models import Home
from news.models import Article
from photo.models import Photo
from recipe.models import Recipe
from vcelnice.serializers.CertificateSerializer import CertificateSerializer
from vcelnice.serializers.ContactSerializer import ContactSerializer
from vcelnice.serializers.HomeSerializer import HomeSerializer
from vcelnice.serializers.NewsSerializer import NewsSerializer
from vcelnice.serializers.PhotoSerializer import PhotoSerializer
from vcelnice.serializers.RecipeSerializer import RecipeSerializer
from vcelnice.serializers.ReservationSerializer import ReservationSerializer
from vcelnice.serializers.VideoSerializer import VideoSerializer
from vcelnice.settings import YOUTUBE_STATUS_PENDING_UPLOAD
from video.models import Video


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


@api_view(["GET"])
def get_cultures(request):
    query_params = request.query_params
    if "locale" in query_params:
        activate(query_params["locale"])
    cultures = {
        "amount_description": _("Number of glasses"),
        "certificates": _("Certificates"),
        "close": _("Close"),
        "contact": _("Contact"),
        "czk": _("CZK"),
        "enter_email": _("Enter a valid email address"),
        "enter_amount": _("Enter amount"),
        "error_empty_message": _("Please enter your message"),
        "home": _("Home"),
        "loading": _("Loading"),
        "news": _("News"),
        "not_in_store": _("Not in store"),
        "ok_message_sent": _("Message was sent, thank you"),
        "photo": _("Photo"),
        "pickup_location": _("Pickup location"),
        "price_list": _("Price list"),
        "prices_not_found": _("Prices not found"),
        "recipes": _("Recipes"),
        "region": _("Region"),
        "reservation_ok": _("Reservation was sent, thank you"),
        "reserve": _("Reserve"),
        "send": _("Send"),
        "server_error": _("Server error, please try again later"),
        "video": _("Video"),
        "your_email": _("Your email address")
    }
    return Response(cultures, status=status.HTTP_200_OK)
