from django.urls import path

from .views import RecipeAPIListView, RecipeAPIRootView

app_name = "recipe-api"

urlpatterns = [
    path("", RecipeAPIRootView.as_view(), name="root"),
    path("list/", RecipeAPIListView.as_view(), name="recipe-list"),
]