import os

from django.test import SimpleTestCase
from django.urls import NoReverseMatch, resolve, reverse


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vcelnice.settings.development")


class ApiRoutingTests(SimpleTestCase):
    def test_api_routes_resolve_to_new_api_package(self):
        home_match = resolve("/api/v1/home/")
        cultures_match = resolve("/api/v1/cultures/")

        self.assertEqual(home_match.func.__module__, "vcelnice.api.views")
        self.assertEqual(cultures_match.func.__module__, "vcelnice.api.views")

    def test_legacy_project_views_module_remains_compatible(self):
        from vcelnice import views

        self.assertEqual(views.home_text.__module__, "vcelnice.api.views")
        self.assertEqual(views.video_list.__module__, "vcelnice.api.views")


class ClientRoutingTests(SimpleTestCase):
    def test_removed_prices_page_uses_the_spa_fallback(self):
        for path in ("/cenik", "/cenik/"):
            with self.subTest(path=path):
                match = resolve(path)

                self.assertEqual(match.url_name, "spa-catch-all")

        with self.assertRaises(NoReverseMatch):
            reverse("prices")

    def test_removed_contact_page_uses_the_spa_fallback(self):
        for path in ("/kontakt", "/kontakt/"):
            with self.subTest(path=path):
                match = resolve(path)

                self.assertEqual(match.url_name, "spa-catch-all")

        with self.assertRaises(NoReverseMatch):
            reverse("contact")
