from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from vcelnice.common.image import ImageUploader
import os


class Article(models.Model):
    objects = models.Manager()
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_("Created"))
    icon = models.ImageField(upload_to="news", max_length=100, null=True, blank=True, verbose_name=_("Thumbnail"))
    id = models.BigAutoField(primary_key=True)
    text = models.TextField(verbose_name=_("Body"))
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=_("Updated"))

    # noinspection PyUnresolvedReferences
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.icon:
            article = Article.objects.filter(icon=self.icon)

            if len(article) == 0:
                uploader = ImageUploader(self.icon)
                image_handle = uploader.save(300, 300)

                image_field = SimpleUploadedFile(self.icon.name, image_handle.read(),
                                                 content_type=self.icon.file.content_type)
                self.icon.save("%s.%s" % (os.path.splitext(self.icon.name)[0], "jpg"), image_field, save=False)
        super(Article, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _("News article")
        verbose_name_plural = _("News")

    def __str__(self):
        return self.title
