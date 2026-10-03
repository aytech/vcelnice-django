from django.urls import path

from .views import PricesAPIRootView, PricesAPIListView

app_name = "prices-api"

urlpatterns = [
    path("", PricesAPIRootView.as_view(), name="root"),
    path("list/", PricesAPIListView.as_view(), name="prices-list"),
    # path("locations/", views.location_list, name="locations-api"),
]
