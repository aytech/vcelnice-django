import tempfile
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from home.models import Home


class HomeModelTests(TestCase):
    @staticmethod
    def create_image():
        image = BytesIO()
        Image.new("RGB", (1600, 800)).save(image, "JPEG")
        return SimpleUploadedFile(
            "home.jpg", image.getvalue(), content_type="image/jpeg"
        )

    def test_save_creates_singleton_and_uses_title_as_string(self):
        home = Home(title="Welcome", text="Home page text")

        home.save()

        self.assertEqual(home.pk, Home.SINGLETON_PK)
        self.assertEqual(str(home), "Welcome")
        self.assertEqual(Home.objects.get(), home)

    def test_save_rejects_second_home_record(self):
        Home.objects.create(title="Existing", text="Existing home page")

        with self.assertRaisesMessage(
            ValidationError,
            "Home text already exist. Update the existing record.",
        ):
            Home(title="Duplicate", text="Duplicate home page").save()

        self.assertEqual(Home.objects.count(), 1)

    def test_save_converts_icon_to_resized_png(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            home = Home(
                title="Welcome",
                text="Home page text",
                icon=self.create_image(),
            )

            home.save()
            home.refresh_from_db()

            self.assertTrue(home.icon.name.endswith(".png"))
            with home.icon.open("rb") as icon, Image.open(icon) as image:
                self.assertEqual(image.format, "PNG")
                self.assertEqual(image.size, (1200, 600))
