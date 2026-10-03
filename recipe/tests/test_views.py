from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from recipe.models import Recipe


class RecipeAPIViewTests(TestCase):
    def test_api_root_links_to_recipe_list(self):
        response = self.client.get(reverse("recipe-api:root"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(
            response.json(),
            {"photos": "http://testserver" + reverse("recipe-api:recipe-list")},
        )

    def test_recipe_list_serializes_recipes_newest_first(self):
        older = Recipe.objects.create(
            title="Older recipe",
            preview="Older preview",
            text="Older recipe text",
        )
        newer = Recipe.objects.create(
            title="Newer recipe",
            preview="Newer preview",
            text="Newer recipe text",
        )
        now = timezone.now()
        Recipe.objects.filter(pk=older.pk).update(updated=now - timedelta(days=1))
        Recipe.objects.filter(pk=newer.pk).update(updated=now)

        response = self.client.get(reverse("recipe-api:recipe-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        recipes = response.json()["recipes"]
        self.assertEqual(
            [recipe["title"] for recipe in recipes],
            ["Newer recipe", "Older recipe"],
        )
        self.assertEqual(recipes[0]["preview"], "Newer preview")
        self.assertEqual(recipes[0]["text"], "Newer recipe text")
        self.assertIsNone(recipes[0]["thumb"])
