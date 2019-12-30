from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import ugettext_lazy as _
from django.db import models
from vcelnice.common.image import ImageUploader
import os


class Home(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Body'))
    icon = models.ImageField(upload_to='news', max_length=100, null=True, blank=True, verbose_name=_('Thumbnail'))

    # noinspection PyUnresolvedReferences
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if hasattr(self.icon.file, 'content_type'):
            uploader = ImageUploader(self.icon, 'png')
            image_handle = uploader.save(300, 300)

            image_field = SimpleUploadedFile(self.icon.name, image_handle.read(),
                                             content_type=self.icon.file.content_type)
            self.icon.save('%s.%s' % (os.path.splitext(self.icon.name)[0], 'png'), image_field, save=False)

        super(Home, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _('Home text')
        verbose_name_plural = _('Home text')

    def __str__(self):
        return self.title
