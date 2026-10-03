from django.urls import path

from .views import HomeAPIRootView, HomeAPIDetailView, CulturesAPIListView

app_name = "home-api"

urlpatterns = [
    path("", HomeAPIRootView.as_view(), name="root"),
    path("cultures/", CulturesAPIListView.as_view(), name="cultures-list"),
    path("detail/", HomeAPIDetailView.as_view(), name="home-detail"),
]