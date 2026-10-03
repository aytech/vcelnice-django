from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.urls import reverse


class ClientViewTests(SimpleTestCase):
  def setUp(self):
    directory = TemporaryDirectory()
    self.addCleanup(directory.cleanup)
    dist = Path(directory.name) / "dist"
    dist.mkdir()
    (dist / "index.html").write_text(
      '<!doctype html><html><body><div id="root"></div>'
      '<script type="module" src="/static/client/app.js"></script>'
      "</body></html>",
      encoding="utf-8",
    )
    templates = deepcopy(settings.TEMPLATES)
    templates[0]["DIRS"] = [dist]
    self.enterContext(override_settings(TEMPLATES=templates))

  def test_index_renders_the_frontend_entry_point(self):
    response = self.client.get(reverse("client:index"))

    self.assertTemplateUsed(response, "index.html")
    self.assertContains(response, '<div id="root"></div>')
    self.assertContains(response, "/static/client/app.js")

  def test_unknown_routes_are_not_rendered_as_the_frontend(self):
    for path in ("/unknown/", "/api/missing", "/static/missing"):
      with self.subTest(path=path):
        self.assertEqual(self.client.get(path).status_code, 404)

  def test_api_auth_is_not_exposed_when_debug_is_disabled(self):
    self.assertFalse(settings.DEBUG)
    self.assertEqual(self.client.get("/api-auth/login/").status_code, 404)
