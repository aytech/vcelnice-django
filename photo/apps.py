from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PhotoConfig(AppConfig):
    name = "photo"
    verbose_name = _("Photo")
