from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("foto/", views.home, name="photo"),
    path("video/", views.home, name="video"),
    path("certifikaty/", views.home, name="certificates"),
    path("region/", views.home, name="region"),
    path("novinky/", views.home, name="news"),
    path("recepty/", views.home, name="recipes"),
    path("cenik/", views.home, name="prices"),
    path("kontakt/", views.home, name="contact"),
]
