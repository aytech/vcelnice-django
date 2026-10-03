import tempfile
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import SimpleTestCase, override_settings
from PIL import Image

from common.images import ImageUploader


class ImageUploaderTests(SimpleTestCase):
    @staticmethod
    def create_image(width, height):
        image = BytesIO()
        Image.new("RGB", (width, height)).save(image, "JPEG")
        image.seek(0)
        return image

    def test_get_new_size_preserves_aspect_ratio(self):
        uploader = ImageUploader(self.create_image(800, 400))

        self.assertEqual(uploader.get_new_size(200, 200), (200, 100))

    def test_get_new_size_does_not_enlarge_small_images(self):
        uploader = ImageUploader(self.create_image(100, 50))

        self.assertEqual(uploader.get_new_size(200, 200), (100, 50))

    def test_save_model_replaces_image_with_resized_jpeg(self):
        image_field = SimpleNamespace(
            name="photo/source.png",
            file=SimpleNamespace(content_type="image/png"),
            save=Mock(),
        )
        model = SimpleNamespace(image=image_field)
        uploader = ImageUploader(self.create_image(800, 400))

        uploader.save_model(model)

        saved_name, saved_image = image_field.save.call_args.args
        self.assertEqual(saved_name, "photo/source.jpg")
        self.assertEqual(saved_image.content_type, "image/png")
        self.assertFalse(image_field.save.call_args.kwargs["save"])
        with Image.open(saved_image) as image:
            self.assertEqual(image.format, "JPEG")
            self.assertEqual(image.size, (200, 100))

    def test_create_thumbnail_returns_png_without_changing_source(self):
        uploader = ImageUploader(self.create_image(800, 400))

        thumbnail = uploader.create_thumbnail(100, 100)

        self.assertEqual(uploader.image.size, (800, 400))
        self.assertEqual(thumbnail.tell(), 0)
        with Image.open(thumbnail) as image:
            self.assertEqual(image.format, "PNG")
            self.assertEqual(image.size, (100, 50))

    def test_clean_image_uses_configured_storage(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            image_path = default_storage.save(
                "photo/image.jpg", ContentFile(b"image-data")
            )

            ImageUploader.clean_image(image_path)

            self.assertFalse(default_storage.exists(image_path))

    @staticmethod
    def test_clean_image_ignores_empty_and_missing_paths():
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            ImageUploader.clean_image("")
            ImageUploader.clean_image("photo/missing.jpg")

    def test_clean_image_rejects_paths_outside_storage(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            with self.assertRaises(SuspiciousFileOperation):
                ImageUploader.clean_image("../outside.jpg")
