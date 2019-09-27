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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

from vcelnice import views
from client import views as client
from django.utils.translation import ugettext_lazy as _

admin.site.site_header = _('Administration')

urlpatterns = [
    # Client UI routes
    url(r'^$', client.home, name='home'),
    url(r'^foto/', client.home, name='photo'),
    url(r'^video/', client.home, name='video'),
    url(r'^certifikaty/', client.home, name='certificates'),
    url(r'^region/', client.home, name='region'),
    url(r'^novinky/', client.home, name='news'),
    url(r'^recepty/', client.home, name='recipes'),
    url(r'^cenik/', client.home, name='prices'),
    url(r'^kontakt/', client.home, name='contact'),

    # Admin section
    url(r'^admin/', admin.site.urls),

    # API routes
    url(r'^api/v1/home/', views.home_text, name='Home GET API'),
    url(r'^api/v1/news/', views.news_list, name='News GET API'),
    url(r'^api/v1/photos/', views.photo_list, name='Photo GET API'),
    url(r'^api/v1/prices/', views.prices_list, name='Prices GET API'),
    url(r'^api/v1/locations/', views.location_list, name='Locations GET API'),
    url(r'^api/v1/recipes/', views.recipe_list, name='Recipe GET API'),
    url(r'^api/v1/certificates/', views.certificate_list, name='Certificates GET API'),
    url(r'^api/v1/videos/', views.video_list, name='Recipe GET API'),
    url(r'^api/v1/reserve/', views.reserve, name='Reservation POST API'),
    url(r'^api/v1/contact/', views.contact, name='Contact POST API'),
    url(r'^api/v1/token/', views.csrf_token, name='CSRF token GET API'),

    # Media
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),

    # Static
    re_path(r'^assets/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    }),

    # Catch all
    url(r'^.*$', client.home, name='home'),
]

