from django.urls import path

from home.views import HomeAPIRootView

urlpatterns = [
    path("", HomeAPIRootView.as_view(), name="home-detail"),
]