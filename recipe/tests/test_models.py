import tempfile
from io import BytesIO
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from recipe.models import Recipe


class RecipeModelTests(TestCase):
    @staticmethod
    def create_image():
        image = BytesIO()
        Image.new("RGB", (600, 300)).save(image, "PNG")
        return SimpleUploadedFile(
            "gingerbread.png", image.getvalue(), content_type="image/png"
        )

    @staticmethod
    def recipe_data():
        return {
            "title": "Honey gingerbread",
            "preview": "Traditional honey recipe",
            "text": "Mix and bake.",
        }

    def test_save_without_thumbnail_and_string_representation(self):
        recipe = Recipe.objects.create(**self.recipe_data())

        self.assertFalse(recipe.thumb)
        self.assertEqual(str(recipe), "Honey gingerbread")

    def test_save_processes_new_thumbnail_but_not_existing_thumbnail(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            recipe = Recipe(**self.recipe_data(), thumb=self.create_image())

            recipe.save()
            recipe.refresh_from_db()

            self.assertTrue(recipe.thumb.name.endswith(".jpg"))
            with recipe.thumb.open("rb") as image_file, Image.open(image_file) as image:
                self.assertEqual(image.format, "JPEG")
                self.assertEqual(image.size, (150, 75))

            with patch("recipe.models.ImageUploader") as image_uploader:
                recipe.preview = "Updated preview"
                recipe.save()

            image_uploader.assert_not_called()
            recipe.refresh_from_db()
            self.assertEqual(recipe.preview, "Updated preview")
