from django.urls import path

from .views import VideoAPIRootView, VideoAPIListView

app_name = "video-api"

urlpatterns = [
    path("", VideoAPIRootView.as_view(), name="root"),
    path("list/", VideoAPIListView.as_view(), name="video-list"),
]