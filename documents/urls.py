from django.urls import path

from .views import CertificatesAPIRootView, CertificatesAPIListView

app_name = "certificates-api"

urlpatterns = [
    path("", CertificatesAPIRootView.as_view(), name="root"),
    path("list/", CertificatesAPIListView.as_view(), name="certificates-list"),
]