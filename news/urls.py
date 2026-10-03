from django.urls import path

from .views import NewsAPIRootView, NewsAPIListView

app_name = "news-api"

urlpatterns = [
    path("", NewsAPIRootView.as_view(), name="root"),
    path("list/", NewsAPIListView.as_view(), name="news-list"),
]