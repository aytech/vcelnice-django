import os

from django.test import SimpleTestCase, override_settings
from django.urls import NoReverseMatch, resolve, reverse

from vcelnice.settings import production as production_settings


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


class ProductionSecurityHeaderTests(SimpleTestCase):
    @override_settings(
        SECURE_REFERRER_POLICY=production_settings.SECURE_REFERRER_POLICY
    )
    def test_referrer_policy_allows_youtube_to_identify_the_site(self):
        response = self.client.get("/api/v1/token/")

        self.assertEqual(
            response.headers["Referrer-Policy"],
            "strict-origin-when-cross-origin",
        )


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

    def test_removed_video_page_uses_the_spa_fallback(self):
        for path in ("/video", "/video/"):
            with self.subTest(path=path):
                match = resolve(path)

                self.assertEqual(match.url_name, "spa-catch-all")

        with self.assertRaises(NoReverseMatch):
            reverse("video")

    def test_removed_certificates_page_uses_the_spa_fallback(self):
        for path in ("/certifikaty", "/certifikaty/"):
            with self.subTest(path=path):
                match = resolve(path)

                self.assertEqual(match.url_name, "spa-catch-all")

        with self.assertRaises(NoReverseMatch):
            reverse("certificates")

    def test_removed_landing_section_pages_use_the_spa_fallback(self):
        removed_routes = {
            "photo": "/foto",
            "region": "/region",
            "news": "/novinky",
            "recipes": "/recepty",
        }

        for route_name, path in removed_routes.items():
            for candidate in (path, f"{path}/"):
                with self.subTest(path=candidate):
                    match = resolve(candidate)

                    self.assertEqual(match.url_name, "spa-catch-all")

            with self.subTest(route_name=route_name):
                with self.assertRaises(NoReverseMatch):
                    reverse(route_name)
