import tempfile
from io import BytesIO
from unittest.mock import call, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from photo.models import Photo


class PhotoModelTests(TestCase):
    @staticmethod
    def create_image():
        image = BytesIO()
        Image.new("RGB", (1200, 600)).save(image, "PNG")
        return SimpleUploadedFile(
            "apiary.png", image.getvalue(), content_type="image/png"
        )

    def test_save_without_image_delegates_without_processing(self):
        photo = Photo(caption="Incomplete photo")

        with patch("django.db.models.Model.save") as model_save, patch(
            "photo.models.ImageUploader"
        ) as image_uploader:
            photo.save()

        model_save.assert_called_once()
        image_uploader.assert_not_called()

    def test_save_processes_new_image_but_not_existing_image(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            photo = Photo(caption="Apiary", image=self.create_image())

            photo.save()
            photo.refresh_from_db()

            self.assertEqual(str(photo), "Apiary")
            self.assertEqual((photo.width, photo.height), (800, 400))
            self.assertTrue(photo.image.name.endswith(".jpg"))
            self.assertTrue(photo.thumb.name.endswith("_thumbnail.png"))

            with photo.image.open("rb") as image_file, Image.open(image_file) as image:
                self.assertEqual(image.format, "JPEG")
                self.assertEqual(image.size, (800, 400))
            with photo.thumb.open("rb") as thumb_file, Image.open(thumb_file) as thumb:
                self.assertEqual(thumb.format, "PNG")
                self.assertEqual(thumb.size, (200, 100))

            with patch("photo.models.ImageUploader") as image_uploader:
                photo.caption = "Updated apiary"
                photo.save()

            image_uploader.assert_not_called()

    def test_delete_removes_image_files_and_record(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            photo = Photo.objects.create(caption="Apiary", image=self.create_image())
            photo_id = photo.pk
            image_storage = photo.image.storage
            image_name = photo.image.name
            thumb_name = photo.thumb.name

            photo.delete()

            self.assertFalse(Photo.objects.filter(pk=photo_id).exists())
            self.assertFalse(image_storage.exists(image_name))
            self.assertFalse(image_storage.exists(thumb_name))

    def test_queryset_delete_cleans_every_photo(self):
        photos = Photo.objects.bulk_create(
            [
                Photo(
                    caption="First",
                    image="photo/first.jpg",
                    thumb="photo/thumb/first.png",
                ),
                Photo(
                    caption="Second",
                    image="photo/second.jpg",
                    thumb="photo/thumb/second.png",
                ),
            ]
        )

        with patch("photo.models.ImageUploader.clean_image") as clean_image:
            Photo.objects.filter(pk__in=[photo.pk for photo in photos]).delete()

        clean_image.assert_has_calls(
            [
                call(image_path="photo/thumb/first.png"),
                call(image_path="photo/first.jpg"),
                call(image_path="photo/thumb/second.png"),
                call(image_path="photo/second.jpg"),
            ],
            any_order=True,
        )
        self.assertEqual(clean_image.call_count, 4)
        self.assertFalse(Photo.objects.exists())
