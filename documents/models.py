from django.db import models
import os
from django.utils.translation import ugettext_lazy as _


class Document(models.Model):
    objects = models.Manager()
    description = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("Description"))
    file = models.FileField(upload_to="documents", verbose_name=_("File"))
    type = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Type"))

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        name, extension = os.path.splitext(self.file.name)

        if extension == ".pdf":
            self.type = "application/pdf"

        if extension == ".doc":
            self.type = "application/msword"

        super(Document, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.description
