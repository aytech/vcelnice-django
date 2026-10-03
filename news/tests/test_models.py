import tempfile
from io import BytesIO
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from news.models import Article


class ArticleModelTests(TestCase):
    @staticmethod
    def create_image():
        image = BytesIO()
        Image.new("RGB", (600, 300)).save(image, "PNG")
        return SimpleUploadedFile(
            "article.png", image.getvalue(), content_type="image/png"
        )

    def test_save_without_icon_and_string_representation(self):
        article = Article.objects.create(title="Apiary news", text="Article body")

        self.assertFalse(article.icon)
        self.assertEqual(str(article), "Apiary news")

    def test_save_processes_new_icon_but_not_existing_icon(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            article = Article(
                title="Apiary news",
                text="Article body",
                icon=self.create_image(),
            )

            article.save()
            article.refresh_from_db()

            self.assertTrue(article.icon.name.endswith(".jpg"))
            with article.icon.open("rb") as icon, Image.open(icon) as image:
                self.assertEqual(image.format, "JPEG")
                self.assertEqual(image.size, (300, 150))

            with patch("news.models.ImageUploader") as image_uploader:
                article.title = "Updated apiary news"
                article.save()

            image_uploader.assert_not_called()
            article.refresh_from_db()
            self.assertEqual(article.title, "Updated apiary news")
