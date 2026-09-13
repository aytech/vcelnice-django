from django.contrib.auth import get_user_model
from django.core.management import get_commands
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from video.forms import VideoForm
from video.models import Video


class VideoAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            username="video-admin", email="admin@example.com", password="test-password"
        )
        cls.video = Video.objects.create(
            caption="Existing video", youtube_id="dQw4w9WgXcQ"
        )

    def setUp(self):
        self.client.force_login(self.admin_user)

    def test_list_add_and_change_pages_render(self):
        response = self.client.get(reverse("admin:video_video_changelist"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.video.caption)
        self.assertNotContains(response, 'class="column-youtube"')

        for url in (
            reverse("admin:video_video_add"),
            reverse("admin:video_video_change", args=[self.video.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                fields = response.context["adminform"].form.fields
                self.assertIn("youtube_id", fields)
                self.assertTrue(fields["youtube_id"].help_text)
                self.assertNotContains(response, 'name="file"')
                self.assertContains(response, 'name="thumb"')
                self.assertTrue(
                    {"file", "category", "tags", "youtube_status", "youtube"}.isdisjoint(fields)
                )

    def test_add_video_with_manually_entered_youtube_id(self):
        response = self.client.post(
            reverse("admin:video_video_add"),
            {
                "caption": "New video",
                "description": "Uploaded manually on YouTube",
                "youtube_id": "_-AbC123xyZ",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)
        video = Video.objects.get(caption="New video")
        self.assertEqual(video.youtube_id, "_-AbC123xyZ")
        self.assertEqual(video.description, "Uploaded manually on YouTube")

    def test_edit_video_updates_manual_youtube_id(self):
        response = self.client.post(
            reverse("admin:video_video_change", args=[self.video.pk]),
            {
                "caption": "Updated video",
                "description": "Updated description",
                "youtube_id": "_-AbC123xyZ",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.video.refresh_from_db()
        self.assertEqual(self.video.caption, "Updated video")
        self.assertEqual(self.video.youtube_id, "_-AbC123xyZ")

    def test_delete_video_removes_record_immediately(self):
        response = self.client.post(
            reverse("admin:video_video_delete", args=[self.video.pk]),
            {"post": "yes"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Video.objects.filter(pk=self.video.pk).exists())

    def test_bulk_delete_removes_records_immediately(self):
        another_video = Video.objects.create(
            caption="Another video", youtube_id="_-AbC123xyZ"
        )
        video_ids = [self.video.pk, another_video.pk]

        response = self.client.post(
            reverse("admin:video_video_changelist"),
            {
                "action": "delete_selected",
                "_selected_action": video_ids,
                "post": "yes",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Video.objects.filter(pk__in=video_ids).exists())

    def test_invalid_youtube_id_is_rejected_without_saving(self):
        for youtube_id in (
            "too-short",
            "dQw4w9WgXcQQ",
            "dQw4w9WgXc!",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ):
            with self.subTest(youtube_id=youtube_id):
                response = self.client.post(
                    reverse("admin:video_video_add"),
                    {"caption": "Invalid video", "youtube_id": youtube_id},
                )

                self.assertEqual(response.status_code, 200)
                self.assertIn("youtube_id", response.context["adminform"].form.errors)

        self.assertFalse(Video.objects.filter(caption="Invalid video").exists())

    def test_form_allows_a_draft_without_youtube_id(self):
        form = VideoForm(data={"caption": "Draft video", "youtube_id": ""})

        self.assertTrue(form.is_valid(), form.errors)
        self.assertFalse(form.save().youtube_id)


class YouTubeCommandRemovalTests(SimpleTestCase):
    def test_youtube_management_commands_are_not_available(self):
        self.assertEqual(
            [name for name in get_commands() if name.startswith("youtube")], []
        )
