from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from video.models import Video


class VideoApiTests(TestCase):
    def test_api_root_links_to_video_list(self):
        response = self.client.get(reverse("video-api:root"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"videos": "http://testserver/api/v1/video/list/"},
        )
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_only_manually_linked_videos_are_published_newest_first(self):
        older = Video.objects.create(
            caption="Older video",
            description="Older description",
            youtube_id="dQw4w9WgXcQ",
        )
        newer = Video.objects.create(
            caption="Newer video",
            description="Newer description",
            youtube_id="_-AbC123xyZ",
        )
        Video.objects.create(caption="Blank ID draft", youtube_id="")
        Video.objects.create(caption="Null ID draft", youtube_id=None)
        now = timezone.now()
        Video.objects.filter(pk=older.pk).update(updated=now - timedelta(days=1))
        Video.objects.filter(pk=newer.pk).update(updated=now)

        response = self.client.get(reverse("video-api:video-list"))

        self.assertEqual(response.status_code, 200)
        videos = response.json()["videos"]
        self.assertEqual(
            [video["youtube_id"] for video in videos],
            [newer.youtube_id, older.youtube_id],
        )
        self.assertEqual(videos[0]["caption"], newer.caption)
        self.assertEqual(videos[0]["description"], newer.description)
        for video in videos:
            self.assertTrue(
                {"caption", "description", "thumb", "created", "updated", "youtube_id"}
                .issubset(video)
            )
            self.assertTrue({"file", "category", "tags", "youtube_status"}.isdisjoint(video))

    def test_no_published_videos_returns_an_empty_list(self):
        Video.objects.create(caption="Draft video", youtube_id="")

        response = self.client.get(reverse("video-api:video-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"videos": []})
