from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PhotoConfig(AppConfig):
    name = "photo"
    verbose_name = _("Photo")
