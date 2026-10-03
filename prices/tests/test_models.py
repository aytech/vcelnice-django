import tempfile
from io import BytesIO
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from prices.models import Price, Reservation


class PriceModelTests(TestCase):
    @staticmethod
    def create_image():
        image = BytesIO()
        Image.new("RGB", (600, 300)).save(image, "PNG")
        return SimpleUploadedFile(
            "honey.png", image.getvalue(), content_type="image/png"
        )

    def test_reservation_uses_title_as_string(self):
        reservation = Reservation(title="Honey reservation")

        self.assertEqual(str(reservation), "Honey reservation")

    def test_save_without_image_delegates_without_processing(self):
        price = Price(title="Honey", price=200)

        with patch("django.db.models.Model.save") as model_save, patch(
            "prices.models.ImageUploader"
        ) as image_uploader:
            price.save()

        model_save.assert_called_once()
        image_uploader.assert_not_called()

    def test_save_processes_new_image_but_not_existing_image(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            price = Price(title="Honey", price=200, image=self.create_image())

            price.save()
            price.refresh_from_db()

            self.assertEqual(str(price), "Honey")
            self.assertTrue(price.image.name.endswith(".jpg"))
            with price.image.open("rb") as image_file, Image.open(image_file) as image:
                self.assertEqual(image.format, "JPEG")
                self.assertEqual(image.size, (200, 100))

            with patch("prices.models.ImageUploader") as image_uploader:
                price.in_store = 10
                price.save()

            image_uploader.assert_not_called()
            price.refresh_from_db()
            self.assertEqual(price.in_store, 10)
