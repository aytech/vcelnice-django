from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from photo.models import Photo


class PhotoAPIViewTests(TestCase):
    def test_api_root_links_to_photo_list(self):
        response = self.client.get(reverse("photo-api:root"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(
            response.json(),
            {"photos": "http://testserver" + reverse("photo-api:photo-list")},
        )

    def test_photo_list_serializes_photos_newest_first(self):
        older, newer = Photo.objects.bulk_create(
            [
                Photo(
                    caption="Older photo",
                    image="photo/older.jpg",
                    thumb="photo/thumb/older.png",
                    width=800,
                    height=400,
                ),
                Photo(
                    caption="Newer photo",
                    image="photo/newer.jpg",
                    thumb="photo/thumb/newer.png",
                    width=600,
                    height=300,
                ),
            ]
        )
        now = timezone.now()
        Photo.objects.filter(pk=older.pk).update(created=now - timedelta(days=1))
        Photo.objects.filter(pk=newer.pk).update(created=now)

        response = self.client.get(reverse("photo-api:photo-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        photos = response.json()["photos"]
        self.assertEqual(
            [photo["caption"] for photo in photos],
            ["Newer photo", "Older photo"],
        )
        self.assertEqual(photos[0]["id"], newer.pk)
        self.assertEqual(photos[0]["image"], "/media/photo/newer.jpg")
        self.assertEqual(photos[0]["thumb"], "/media/photo/thumb/newer.png")
        self.assertEqual((photos[0]["width"], photos[0]["height"]), (600, 300))
        self.assertIn("created", photos[0])
