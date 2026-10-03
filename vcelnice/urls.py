"""Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _('Administration')

urlpatterns = [
    # Admin section
    path("admin/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),

    # API routes
    path("api/v1/home/", include("home.urls")),
    path("api/v1/prices/", include("prices.urls")),
    path("api/v1/certificates/", include("documents.urls")),
    path("api/v1/news/", include("news.urls")),
    path("api/v1/photo/", include("photo.urls")),
    path("api/v1/recipe/", include("recipe.urls")),
    path("api/v1/video/", include("video.urls")),
]

if settings.DEBUG:
    urlpatterns.append(
        path("api-auth/", include("rest_framework.urls")),
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("", include("client.urls")),
]
