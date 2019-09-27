from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import ugettext_lazy as _
from vcelnice.common.image import ImageUploader
import os


class Recipe(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Title'))
    thumb = models.ImageField(upload_to='recipe', max_length=100, null=True, blank=True, verbose_name=_('Thumbnail'))
    preview = models.TextField(null=False, blank=False, verbose_name=_('Preview'),
                               help_text=_('Preview for recipe thumbnails, maximum 150 characters'))
    text = models.TextField(null=False, blank=False, verbose_name=_('Recipe text'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=_('Updated'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.thumb:
            recipe = Recipe.objects.filter(thumb=self.thumb)

            if len(recipe) == 0:
                uploader = ImageUploader(self.thumb)
                image_handle = uploader.save(150, 150)

                image_field = SimpleUploadedFile(self.thumb.name, image_handle.read(),
                                                 content_type=self.thumb.file.content_type)

                self.thumb.save('%s.%s' % (os.path.splitext(self.thumb.name)[0], 'jpg'), image_field, save=False)

        super(Recipe, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title
