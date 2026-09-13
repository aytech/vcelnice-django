import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from vcelnice.common.image import ImageUploader
from vcelnice.common.translit import Translit


class Video(models.Model):
    objects = models.Manager()

    caption = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("Caption"))
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    file = models.FileField(upload_to="youtube", max_length=150, blank=True, verbose_name=_("File"))
    id = models.BigAutoField(primary_key=True)
    thumb = models.ImageField(upload_to="video", max_length=150, null=True, blank=True, verbose_name=_("Thumbnail"))
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    youtube_id = models.CharField(
        max_length=150, null=True, blank=True, verbose_name=_("YouTube video ID"),
        help_text=_("Upload the video to YouTube manually and enter its 11-character ID, not the full URL. "
                    "Leave blank to hide the video from the website."),
        validators=[RegexValidator(
            regex=r"\A[a-zA-Z0-9_-]{11}\Z",
            message=_("Enter a valid 11-character YouTube video ID."),
        )],
    )

    def save(self, *args, **kwargs):
        if self.thumb:
            video = Video.objects.filter(thumb=self.thumb)
            if len(video) == 0:
                uploader = ImageUploader(self.thumb)
                image_handle = uploader.save(200, 200)
                image_field = SimpleUploadedFile(
                    self.thumb.name,
                    image_handle.read(),
                    content_type=self.thumb.file.content_type,
                )
                self.thumb.save(
                    "%s.%s" % (os.path.splitext(self.thumb.name)[0], "jpg"),
                    image_field,
                    save=False,
                )
        if self.file:
            self.file.name = Translit.translit(self.file.name)

        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")
