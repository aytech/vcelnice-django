from django.urls import path

from vcelnice.api import views


urlpatterns = [
    path("home/", views.home_text, name="home-api"),
    path("news/", views.news_list, name="news-api"),
    path("photos/", views.photo_list, name="photo-api"),
    path("recipes/", views.recipe_list, name="recipe-api"),
    path("certificates/", views.certificate_list, name="certificates-api"),
    path("videos/", views.video_list, name="videos-api"),
    path("reserve/", views.reserve, name="reservation-api"),
    path("contact/", views.contact, name="contact-api"),
    path("token/", views.csrf_token, name="csrf-token-api"),
    path("cultures/", views.get_cultures, name="cultures-api"),
]
