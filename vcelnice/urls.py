"""vcelnice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import re_path
from django.utils.translation import gettext_lazy as _
from django.views.static import serve

from client import views as client
from prices import views as prices
from vcelnice import views

admin.site.site_header = _('Administration')

urlpatterns = [
    # Client UI routes
    re_path(r'^$', client.home, name='home'),
    re_path(r'^foto/', client.home, name='photo'),
    re_path(r'^video/', client.home, name='video'),
    re_path(r'^certifikaty/', client.home, name='certificates'),
    re_path(r'^region/', client.home, name='region'),
    re_path(r'^novinky/', client.home, name='news'),
    re_path(r'^recepty/', client.home, name='recipes'),
    re_path(r'^cenik/', client.home, name='prices'),
    re_path(r'^kontakt/', client.home, name='contact'),

    # Admin section
    re_path(r'^admin/', admin.site.urls),

    # API routes
    re_path(r'^api/v1/home/', views.home_text, name='Home GET API'),
    re_path(r'^api/v1/news/', views.news_list, name='News GET API'),
    re_path(r'^api/v1/photos/', views.photo_list, name='Photo GET API'),
    re_path(r'^api/v1/prices/', prices.prices_list, name='Prices GET API'),
    re_path(r'^api/v1/locations/', prices.location_list, name='Locations GET API'),
    re_path(r'^api/v1/recipes/', views.recipe_list, name='Recipe GET API'),
    re_path(r'^api/v1/certificates/', views.certificate_list, name='Certificates GET API'),
    re_path(r'^api/v1/videos/', views.video_list, name='Recipe GET API'),
    re_path(r'^api/v1/reserve/', views.reserve, name='Reservation POST API'),
    re_path(r'^api/v1/contact/', views.contact, name='Contact POST API'),
    re_path(r'^api/v1/token/', views.csrf_token, name='CSRF token GET API'),
    re_path(r'^api/v1/cultures/', views.get_cultures, name='Get translations'),

    # Media
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),

    # Static
    re_path(r'^assets/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    }),

    # Catch all
    re_path(r'^.*$', client.home, name='home'),
]

