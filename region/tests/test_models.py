from django.db import models as django_models
from django.test import SimpleTestCase

from region import models as region_models


class RegionModelsTests(SimpleTestCase):
    def test_models_module_imports_django_models(self):
        self.assertIs(region_models.models, django_models)
