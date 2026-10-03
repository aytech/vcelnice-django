from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import gettext_lazy as _
from django.db import models
from common.images import ImageUploader
import os


class Home(models.Model):
    SINGLETON_PK = 1

    objects = models.Manager()
    icon = models.ImageField(upload_to='news', max_length=100, null=True, blank=True, verbose_name=_('Thumbnail'))
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Body'))

    # noinspection PyUnresolvedReferences
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.pk = self.SINGLETON_PK

        if (
            self._state.adding
            and type(self).objects.filter(pk=self.SINGLETON_PK).exists()
        ):
            raise ValidationError(_("Home text already exist. Update the existing record."))

        if self.icon and hasattr(self.icon.file, 'content_type'):
            uploader = ImageUploader(self.icon, 'png')
            image_handle = uploader.save(1200, 1200)

            image_field = SimpleUploadedFile(self.icon.name, image_handle.read(),
                                             content_type=self.icon.file.content_type)
            self.icon.save(f'{os.path.splitext(self.icon.name)[0]}.png', image_field, save=False)

        self.full_clean()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields)

    class Meta:
        verbose_name = _('Home text')
        verbose_name_plural = _('Home text')

    def __str__(self):
        return self.title
