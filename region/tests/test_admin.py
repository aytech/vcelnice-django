from django.contrib import admin as django_admin
from django.test import SimpleTestCase

from region import admin as region_admin


class RegionAdminTests(SimpleTestCase):
    def test_admin_module_imports_django_admin(self):
        self.assertIs(region_admin.admin, django_admin)
