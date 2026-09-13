from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import FileField
from django.test import SimpleTestCase

from video.forms import VideoForm


class ManualVideoFormTests(SimpleTestCase):
    def test_manual_youtube_link_does_not_require_a_local_video_file(self):
        form = VideoForm(data={'caption': 'Manual video', 'youtube_id': 'qH6i5JsntCw'})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertNotIn('file', form.fields)
        self.assertNotIn('file', form.cleaned_data)

    def test_thumbnail_is_the_only_file_upload_control(self):
        form = VideoForm()
        uploads = {name for name, field in form.fields.items() if isinstance(field, FileField)}
        self.assertEqual(uploads, {'thumb'})
        self.assertFalse(form.fields['thumb'].required)

    def test_original_video_upload_is_not_bound_to_the_model(self):
        form = VideoForm(
            data={'caption': 'Video', 'youtube_id': 'qH6i5JsntCw'},
            files={'file': SimpleUploadedFile('original.mp4', b'video-bytes')},
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertNotIn('file', form.cleaned_data)
        self.assertFalse(hasattr(form.save(commit=False), 'file'))
