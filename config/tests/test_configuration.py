from importlib import import_module, reload

from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.urls import clear_url_caches


class ProjectConfigurationTests(SimpleTestCase):
    def test_django_entry_points_use_config_package(self):
        self.assertEqual(settings.ROOT_URLCONF, "config.urls")
        self.assertEqual(settings.WSGI_APPLICATION, "config.wsgi.application")

    def test_config_modules_are_importable(self):
        self.assertIsNotNone(import_module(settings.ROOT_URLCONF))
        self.assertIsNotNone(
            import_module(settings.WSGI_APPLICATION.rpartition(".")[0])
        )
        self.assertIsNotNone(import_module("config.asgi"))

    def test_debug_urls_include_api_authentication_and_media(self):
        urlconf = import_module(settings.ROOT_URLCONF)

        try:
            with override_settings(DEBUG=True):
                debug_urlconf = reload(urlconf)
                routes = [str(pattern.pattern) for pattern in debug_urlconf.urlpatterns]

                self.assertIn("api-auth/", routes)
                self.assertIn(r"^media/(?P<path>.*)$", routes)
        finally:
            reload(urlconf)
            clear_url_caches()
