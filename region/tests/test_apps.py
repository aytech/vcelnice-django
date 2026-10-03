from django.apps import AppConfig
from django.test import SimpleTestCase

from region.apps import RegionConfig


class RegionConfigTests(SimpleTestCase):
    def test_region_config(self):
        self.assertTrue(issubclass(RegionConfig, AppConfig))
        self.assertEqual(RegionConfig.name, "region")
