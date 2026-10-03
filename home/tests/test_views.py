from django.test import TestCase
from django.urls import reverse

from home.models import Home


class HomeAPIViewTests(TestCase):
    def test_api_root_links_to_detail_and_cultures(self):
        response = self.client.get(reverse("home-api:root"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(
            response.json(),
            {
                "detail": "http://testserver" + reverse("home-api:home-detail"),
                "cultures": (
                    "http://testserver" + reverse("home-api:cultures-list")
                ),
            },
        )

    def test_detail_returns_empty_resource_when_home_is_not_configured(self):
        response = self.client.get(reverse("home-api:home-detail"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(
            response.json(),
            {"id": None, "title": "", "text": "", "icon": None},
        )

    def test_detail_serializes_configured_home(self):
        home = Home.objects.create(title="Welcome", text="Home page text")

        response = self.client.get(reverse("home-api:home-detail"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": home.pk,
                "title": "Welcome",
                "text": "Home page text",
                "icon": None,
            },
        )

    def test_cultures_returns_supported_locale(self):
        response = self.client.get(
            reverse("home-api:cultures-list"), {"locale": "en"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(len(response.json()), 18)
        self.assertEqual(response.json()["home"], "Home")
        self.assertEqual(response.json()["your_email"], "Your email address")

    def test_cultures_rejects_unsupported_locale(self):
        response = self.client.get(
            reverse("home-api:cultures-list"), {"locale": "de"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})
