import math
import os
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from vcelnice import settings


class ImageUploader:
    def __init__(self, image, ext="jpeg"):
        self.image = Image.open(BytesIO(image.read())).convert('RGB')
        self.IMAGE_TYPE = ext
        self.THUMBNAIL_EXTENSION = "png"

    def save(self, to_width, to_height):
        size = self.get_new_size(to_width, to_height)
        self.image = self.image.resize(size, Image.Resampling.LANCZOS)

        temp_handle = BytesIO()
        self.image.save(temp_handle, self.IMAGE_TYPE)
        temp_handle.seek(0)

        return temp_handle

    def save_model(self, model):
        # self.image = Image.open(BytesIO(model.image.read()))
        image_handle = self.save(200, 200)
        image_field = SimpleUploadedFile(model.image.name, image_handle.read(),
                                         content_type=model.image.file.content_type)
        model.image.save('%s.%s' % (os.path.splitext(model.image.name)[0], 'jpg'), image_field, save=False)

    def create_thumbnail(self, to_width, to_height):
        thumbnail = self.image.copy()
        thumbnail.thumbnail((to_width, to_height), Image.Resampling.LANCZOS)

        temp_handle = BytesIO()
        thumbnail.save(temp_handle, self.THUMBNAIL_EXTENSION)
        temp_handle.seek(0)

        return temp_handle

    def get_new_size(self, to_width, to_height):
        image_width, image_height = self.image.size

        if image_width < to_width and image_height < to_height:
            return image_width, image_height

        vertical_factor = to_height / image_height
        horizontal_factor = to_width / image_width

        image_factor = min(vertical_factor, horizontal_factor)

        new_height = image_height * image_factor
        new_width = image_width * image_factor

        return math.floor(new_width), math.floor(new_height)

    @staticmethod
    def clean_image(image_path):
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, image_path))
        except FileNotFoundError:
            pass

    def __str__(self):
        pass
