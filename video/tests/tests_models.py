import os
import tempfile
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from PIL import Image

from video.models import Video
from video.models import VideoCategory


class VideoTestCase(TestCase):
    def setUp(self):
        self.media_root = tempfile.TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self.media_root.name)
        self.override.enable()

        VideoCategory.objects.create(category_id="1", title="Category 1")
        VideoCategory.objects.create(category_id="2", title="Category 2")

    def tearDown(self):
        self.override.disable()
        self.media_root.cleanup()

    @staticmethod
    def make_thumb(name="test image.jpg"):
        image = Image.new("RGB", (10, 10), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")

    @staticmethod
    def make_video_file(name="test video.wmv"):
        return SimpleUploadedFile(name, b"video-bytes", content_type="video/x-ms-wmv")

    def create_video(self, **overrides):
        data = {
            "caption": "Testing Video",
            "description": "Testing Video description",
            "category": "1",
            "tags": "vcelnice, vcelka, med",
            "file": self.make_video_file(),
            "thumb": self.make_thumb(),
        }
        data.update(overrides)
        return Video.objects.create(**data)

    def test_video_created_defaults_to_pending_upload(self):
        video = self.create_video()

        self.assertEqual(settings.YOUTUBE_STATUS_PENDING_UPLOAD, video.youtube_status)
        self.assertTrue(video.file.name.endswith(".wmv"))
        self.assertNotIn(" ", os.path.basename(video.file.name))
        self.assertTrue(video.thumb.name.endswith(".jpg"))

    def test_uploaded_video_is_marked_for_update_on_save(self):
        video = self.create_video(youtube_status=settings.YOUTUBE_STATUS_UPLOADED)

        self.assertEqual(settings.YOUTUBE_STATUS_PENDING_UPDATE, video.youtube_status)

    def test_delete_pending_upload_video_removes_record(self):
        video = self.create_video()
        video_id = video.id

        video.delete()

        self.assertFalse(Video.objects.filter(id=video_id).exists())

    def test_delete_uploaded_video_marks_pending_delete(self):
        video = self.create_video(youtube_status=settings.YOUTUBE_STATUS_UPLOADED)

        video.delete()

        video.refresh_from_db()
        self.assertEqual(settings.YOUTUBE_STATUS_PENDING_DELETE, video.youtube_status)
