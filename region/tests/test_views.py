from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from region.views import home


class RegionViewTests(SimpleTestCase):
    @patch("region.views.render")
    def test_home_renders_legacy_region_template(self, render):
        request = RequestFactory().get("/region/")
        response = object()
        render.return_value = response

        self.assertIs(home(request), response)
        render.assert_called_once_with(request, "region.html", {})
