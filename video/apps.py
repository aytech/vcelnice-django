from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VideoConfig(AppConfig):
    name = "video"
    verbose_name = _("Videos")
