from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from vcelnice.common.image import ImageUploader
import os


class Reservation(models.Model):
    amount = models.IntegerField(default=1, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Price(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    weight = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='prices/', max_length=100, null=False, blank=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.image:
            image = Price.objects.filter(image=self.image)

            if len(image) == 0:
                uploader = ImageUploader(self.image)
                image_handle = uploader.save(200, 200)

                image_field = SimpleUploadedFile(self.image.name, image_handle.read(),
                                                 content_type=self.image.file.content_type)

                self.image.save('%s.%s' % (os.path.splitext(self.image.name)[0], 'jpg'), image_field, save=False)

        super(Price, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title
