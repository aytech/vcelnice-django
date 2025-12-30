from django.core.exceptions import ObjectDoesNotExist
from django.middleware.csrf import get_token
from django.utils.translation import activate, gettext_lazy as _, deactivate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from documents.models import Document
from home.models import Home
from news.models import Article
from photo.models import Photo
from recipe.models import Recipe
from vcelnice.common.email import Email, EmailException
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
            serializer.save()  # Just for auditing, will not be used for sending
            # Fix email sending, since Sendgrid expired
            Email().send_reservation_email(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def contact(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Just for auditing, will not be used for sending
            try:
                Email().send_contact_email(serializer)
            except EmailException:
                return Response(_("Failed to send email"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_cultures(request):
    query_params = request.query_params
    cultures = {}

    if "locale" in query_params and query_params["locale"] in ["cs", "en"]:
        activate(query_params["locale"])

        cultures["amount_description"] = _("Number of glasses")
        cultures["certificates"] = _("Certificates")
        cultures["close"] = _("Close")
        cultures["contact"] = _("Contact")
        cultures["czk"] = _("CZK")
        cultures["home"] = _("Home")
        cultures["loading"] = _("Loading")
        cultures["not_in_store"] = _("Not in store")
        cultures["ok_message_sent"] = _("Message was sent, thank you")
        cultures["photo"] = _("Photo")
        cultures["price_list"] = _("Price list")
        cultures["prices_not_found"] = _("Prices not found")
        cultures["recipes"] = _("Recipes")
        cultures["region"] = _("Region")
        cultures["reservation_text"] = _("For reservation, please contact Jan Šaroch at")
        cultures["reserve"] = _("Reserve")
        cultures["video"] = _("Video")
        cultures["your_email"] = _("Your email address")

        deactivate()

    return Response(cultures, status=status.HTTP_200_OK)
