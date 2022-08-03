from django.db import models
from vcelnice.common.image import ImageUploader
from vcelnice.common.translit import Translit
from django.utils.translation import gettext_lazy as _
from vcelnice.settings import *


class Video(models.Model):
    objects = models.Manager()
    CATEGORY_CHOICES = []

    caption = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("Caption"))
    category = models.CharField(max_length=100, null=True, blank=True, choices=CATEGORY_CHOICES,
                                verbose_name=_("Category"))
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    file = models.FileField(upload_to="youtube", max_length=150, null=False, blank=False, verbose_name=_("File"))
    id = models.BigAutoField(primary_key=True)
    thumb = models.ImageField(upload_to="video", max_length=150, null=True, blank=True, verbose_name=_("Thumbnail"))
    tags = models.CharField(max_length=100, null=True, blank=True,
                            help_text=_("Add tags to the video, separated by commas"),
                            verbose_name=_("Tags"))
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    youtube_id = models.CharField(max_length=150, null=True, blank=True)
    youtube_status = models.IntegerField(default=YOUTUBE_STATUS_PENDING_UPLOAD, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.thumb:
            video = Video.objects.filter(thumb=self.thumb)
            if len(video) == 0:
                uploader = ImageUploader(self.thumb)
                uploader.save_model(self)
        self.file.name = Translit.translit(self.file.name)

        if self.youtube_status > YOUTUBE_STATUS_PENDING_UPLOAD:
            self.youtube_status = YOUTUBE_STATUS_PENDING_UPDATE

        super(Video, self).save(*args, **kwargs)

    def save_upload_status(self, status):
        self.youtube_status = status
        super(Video, self).save()

    def delete(self, using=None, keep_parents=False):
        deleted = self.youtube_status == YOUTUBE_STATUS_DELETED
        not_uploaded = self.youtube_status == YOUTUBE_STATUS_PENDING_UPLOAD
        if deleted or not_uploaded:
            super(Video, self).delete(using, keep_parents)
        else:
            self.youtube_status = YOUTUBE_STATUS_PENDING_DELETE
            super(Video, self).save()

    def get_categories(self):
        # noinspection PyUnresolvedReferences
        for category in VideoCategory.objects.all():
            self.CATEGORY_CHOICES.append((category.category_id, category.title))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_categories()

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")


class VideoCategory(models.Model):
    category_id = models.CharField(max_length=10, null=False, blank=False)
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
