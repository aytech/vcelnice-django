from django.db import models
from vcelnice.common.image import ImageUploader
from vcelnice.common.translit import Translit
from vcelnice.common.youtube import Youtube
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import ugettext_lazy as _
from vcelnice.settings import *
import os


class Video(models.Model):
    youtube = Youtube()
    CATEGORY_CHOICES = youtube.get_categories()

    caption = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Caption'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    file = models.FileField(upload_to='youtube', max_length=150, null=False, blank=False, verbose_name=_('File'))
    thumb = models.ImageField(upload_to='video', max_length=150, null=True, blank=True, verbose_name=_('Thumbnail'))
    category = models.CharField(max_length=100, null=True, blank=True, choices=CATEGORY_CHOICES,
                                verbose_name=_('Category'))
    tags = models.CharField(max_length=100, null=True, blank=True,
                            help_text=_('Add tags to the video, separated by commas'),
                            verbose_name=_('Tags'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    youtube_id = models.CharField(max_length=150, null=True, blank=True)
    youtube_status = models.IntegerField(default=YOUTUBE_STATUS_PENDING_UPLOAD, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.thumb:
            video = Video.objects.filter(thumb=self.thumb)

            if len(video) == 0:
                uploader = ImageUploader(self.thumb)
                image_handle = uploader.save(200, 200)

                image_field = SimpleUploadedFile(self.thumb.name, image_handle.read(),
                                                 content_type=self.thumb.file.content_type)

                self.thumb.save('%s.%s' % (os.path.splitext(self.thumb.name)[0], 'jpg'), image_field, save=False)

        self.file.name = Translit.translit(self.file.name)

        if self.youtube_status > YOUTUBE_STATUS_PENDING_UPLOAD:
            self.youtube_status = YOUTUBE_STATUS_PENDING_UPDATE

        super(Video, self).save(*args, **kwargs)

    def save_upload_status(self):
        self.youtube_status = YOUTUBE_STATUS_UPLOADED
        super(Video, self).save()

    def delete(self, using=None, keep_parents=False):
        deleted = self.youtube_status == YOUTUBE_STATUS_DELETED
        not_uploaded = self.youtube_status == YOUTUBE_STATUS_PENDING_UPLOAD

        if deleted or not_uploaded:
            super(Video, self).delete(using, keep_parents)
        else:
            self.youtube_status = YOUTUBE_STATUS_PENDING_DELETE
            super(Video, self).save()

    def save_deleted_status(self):
        self.youtube_status = YOUTUBE_STATUS_DELETED
        super(Video, self).save()

    def __str__(self):
        return self.caption
