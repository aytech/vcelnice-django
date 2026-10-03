from django.urls import path

from .views import HomeAPIRootView, HomeAPIDetailView

app_name = "home-api"

urlpatterns = [
    path("", HomeAPIRootView.as_view(), name="root"),
    path("detail/", HomeAPIDetailView.as_view(), name="home-detail"),
]