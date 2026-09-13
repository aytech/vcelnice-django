import tempfile
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from PIL import Image

from video.models import Video


class VideoTestCase(TestCase):
    def setUp(self):
        self.media_root = tempfile.TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self.media_root.name)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        self.media_root.cleanup()

    @staticmethod
    def make_thumb(name="test image.jpg"):
        image = Image.new("RGB", (10, 10), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")

    def create_video(self, **overrides):
        data = {
            "caption": "Testing Video",
            "description": "Testing Video description",
            "youtube_id": "qH6i5JsntCw",
            "thumb": self.make_thumb(),
        }
        data.update(overrides)
        return Video.objects.create(**data)

    def test_optional_thumbnail_keeps_existing_processing(self):
        video = self.create_video()

        self.assertEqual("qH6i5JsntCw", video.youtube_id)
        self.assertTrue(video.thumb.name.endswith(".jpg"))

    def test_video_can_be_created_without_uploading_files(self):
        video = Video(caption="Manual YouTube video", youtube_id="qH6i5JsntCw")
        video.full_clean()
        video.save()
        video.refresh_from_db()

        self.assertEqual("qH6i5JsntCw", video.youtube_id)
        self.assertNotIn("file", {field.name for field in Video._meta.fields})
        self.assertFalse(video.thumb)

    def test_metadata_update_keeps_manual_youtube_id(self):
        video = self.create_video()
        video.caption = "Updated caption"
        video.save()
        video.refresh_from_db()

        self.assertEqual("Updated caption", video.caption)
        self.assertEqual("qH6i5JsntCw", video.youtube_id)

    def test_delete_video_removes_record_immediately(self):
        for youtube_id in (None, "", "qH6i5JsntCw"):
            with self.subTest(youtube_id=youtube_id):
                video = self.create_video(youtube_id=youtube_id)
                video_id = video.id
                video.delete()
                self.assertFalse(Video.objects.filter(id=video_id).exists())

    def test_model_instantiation_no_longer_queries_categories(self):
        with self.assertNumQueries(0):
            Video(caption="No category lookup")

    def test_youtube_id_validation_rejects_full_urls_and_malformed_ids(self):
        for youtube_id in ("short", "https://youtu.be/qH6i5JsntCw", "qH6i5JsntCw?x=1", "qH6i5JsntCw\n"):
            with self.subTest(youtube_id=youtube_id):
                video = Video(caption="Invalid ID", youtube_id=youtube_id)
                with self.assertRaises(ValidationError) as error:
                    video.full_clean()
                self.assertIn("youtube_id", error.exception.message_dict)
