from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from video.management.commands.youtube import Command
from video.models import Video
from vcelnice.common.youtube import Youtube
from vcelnice.settings import *


class VideoTestCase(TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        thumb_path = os.path.join(path, 'test.jpg')
        video_path = os.path.join(path, 'test.wmv')
        self.youtube = Youtube()

        video = Video()
        video.caption = 'Testing Video'
        video.description = 'Testing Video description'
        video.category = self.youtube.get_categories()[0][0]
        video.tags = 'vcelnice, vcelka, med'
        video.file = SimpleUploadedFile('test.wmv', bytes(video_path, 'utf-8'), content_type='video/x-ms-wmv')
        video.thumb = SimpleUploadedFile('test.jpg', open(thumb_path, 'rb').read(), content_type='image/jpeg')
        video.save()

    def test_video_created(self):
        video = Video.objects.get(caption='Testing Video')
        self.assertEqual(YOUTUBE_STATUS_PENDING_UPLOAD, video.youtube_status)

        cron = Command()
        cron.handle()
        uploaded_videos = self.youtube.get_uploaded_videos()

        video_updated = Video.objects.get(caption='Testing Video')
        self.assertIn(video_updated.youtube_id, uploaded_videos)

    def test_video_updated(self):
        cron = Command()
        cron.handle()

        video = Video.objects.get(caption='Testing Video')
        video.caption = 'Testing Video UPDATED'
        video.description = 'Testing Video description UPDATED'
        video.tags += ', UPDATED'
        category = self.youtube.get_categories()[1][0]
        video.category = category
        video.save()

        cron = Command()
        cron.handle()

        video_updated = Video.objects.get(caption='Testing Video UPDATED')
        uploaded_video = self.youtube.get_uploaded_video(video_updated.youtube_id)

        self.assertEqual(video_updated.caption, uploaded_video['title'])
        self.assertEqual(video_updated.description, uploaded_video['description'])
        self.assertEqual(video_updated.category, uploaded_video['categoryId'])
        self.assertEqual(video_updated.tags.split(', '), uploaded_video['tags'])
        self.assertEqual(video_updated.category, uploaded_video['categoryId'])

        video_updated.caption = 'Testing Video'
        video_updated.save()

    def tearDown(self):
        videos = Video.objects.all()

        for video in videos:
            print('Removing video with youtube ID %s' % video.youtube_id)
            os.remove(os.path.join(MEDIA_ROOT, video.thumb.name))
            os.remove(os.path.join(MEDIA_ROOT, video.file.name))
            if video.youtube_id != '':
                self.youtube.delete_video(video.youtube_id)
