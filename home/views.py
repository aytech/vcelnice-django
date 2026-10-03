from django.utils.translation import activate, deactivate, gettext as _
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
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
    @staticmethod
    def get(request):
        return Response({
            "detail": reverse(
                "home-api:home-detail",
                request=request,
            ),
            "cultures": reverse(
                "home-api:cultures-list",
                request=request,
            )
        })

class HomeAPIDetailView(PublicReadOnlyAPIView):
    """
    Return the single public home resource.
    """
    @staticmethod
    def get(_):
        home = Home.objects.filter(
            pk=Home.SINGLETON_PK,
        ).first()

        if home is None:
            home = Home()

        serializer = HomeSerializer(home)

        return Response(serializer.data)

class CulturesAPIListView(PublicReadOnlyAPIView):
    @staticmethod
    def get(request):
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

        return Response(cultures)
