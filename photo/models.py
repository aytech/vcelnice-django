from django.db import models

from vcelnice import settings
from vcelnice.common.image import ImageUploader
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class PhotoQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for photo in self:
            ImageUploader.clean_image(image_path=photo.thumb.__str__())
            ImageUploader.clean_image(image_path=photo.image.__str__())
        super(PhotoQuerySet, self).delete()


class Photo(models.Model):
    objects = PhotoQuerySet.as_manager()
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photo/', max_length=250, null=False, blank=False)
    thumb = models.ImageField(upload_to='photo/thumb/', max_length=250, null=False, blank=False)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.image:
            photo = Photo.objects.filter(image=self.image)

            if len(photo) == 0:
                uploader = ImageUploader(self.image)
                image_handle = uploader.save(800, 600)
                thumb_handle = uploader.create_thumbnail(200, 200)

                image_field = SimpleUploadedFile(self.image.name, image_handle.read(),
                                                 content_type=self.image.file.content_type)
                thumb_field = SimpleUploadedFile(self.image.name, thumb_handle.read(),
                                                 content_type=self.image.file.content_type)

                self.image.save('%s.%s' % (os.path.splitext(self.image.name)[0], 'jpg'), image_field, save=False)
                self.thumb.save('%s_thumbnail.%s' % (os.path.splitext(self.image.name)[0], 'png'), thumb_field,
                                save=False)
                self.width = self.image.width
                self.height = self.image.height
        super(Photo, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        ImageUploader.clean_image(image_path=self.thumb.__str__())
        ImageUploader.clean_image(image_path=self.image.__str__())
        super(Photo, self).delete(using, keep_parents)

    def __str__(self):
        return self.caption
