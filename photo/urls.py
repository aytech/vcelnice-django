from django.urls import path

from .views import PhotoAPIRootView, PhotoAPIListView

app_name = "photo-api"

urlpatterns = [
    path("", PhotoAPIRootView.as_view(), name="root"),
    path("list/", PhotoAPIListView.as_view(), name="photo-list"),
]