from django.urls import path

from . import views


urlpatterns = [
    path("prices/", views.prices_list, name="prices-api"),
    path("locations/", views.location_list, name="locations-api"),
]
