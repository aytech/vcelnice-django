"""vcelnice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _
from django.views.static import serve

from client import views as client_views

admin.site.site_header = _('Administration')

urlpatterns = [
    # Client UI routes
    path("", include("client.urls")),

    # Admin section
    path("admin/", admin.site.urls),

    # API routes
    path("api/v1/", include("vcelnice.api_urls")),
    path("api/v1/", include("prices.urls")),

    # Media
    path("media/<path:path>", serve, {
        'document_root': settings.MEDIA_ROOT,
    }),

    # Static
    path("assets/<path:path>", serve, {
        'document_root': settings.STATIC_ROOT,
    }),

    # Catch all
    re_path(r"^.*$", client_views.home, name="spa-catch-all"),
]
