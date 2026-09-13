from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from video.forms import VideoForm


class OptionalVideoFileTests(SimpleTestCase):
    def test_manual_youtube_link_does_not_require_a_local_video_file(self):
        form = VideoForm(data={'caption': 'Manual video', 'youtube_id': 'qH6i5JsntCw'})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertFalse(form.cleaned_data['file'])

    def test_optional_local_attachment_accepts_supported_extensions_case_insensitively(self):
        for filename in ('original.wmv', 'original.MP4'):
            with self.subTest(filename=filename):
                form = VideoForm(
                    data={'caption': 'Video'},
                    files={'file': SimpleUploadedFile(filename, b'video-bytes')},
                )
                self.assertTrue(form.is_valid(), form.errors)

    def test_optional_local_attachment_rejects_unsupported_extensions(self):
        form = VideoForm(
            data={'caption': 'Video'},
            files={'file': SimpleUploadedFile('video.html', b'not a video')},
        )
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)
