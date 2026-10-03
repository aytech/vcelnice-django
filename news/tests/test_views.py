from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from news.models import Article


class NewsAPIViewTests(TestCase):
    def test_api_root_links_to_news_list(self):
        response = self.client.get(reverse("news-api:root"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(
            response.json(),
            {"news": "http://testserver" + reverse("news-api:news-list")},
        )

    def test_news_list_serializes_articles_newest_first(self):
        older = Article.objects.create(title="Older news", text="Older article")
        newer = Article.objects.create(title="Newer news", text="Newer article")
        now = timezone.now()
        Article.objects.filter(pk=older.pk).update(updated=now - timedelta(days=1))
        Article.objects.filter(pk=newer.pk).update(updated=now)

        response = self.client.get(reverse("news-api:news-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        articles = response.json()["news"]
        self.assertEqual(
            [article["title"] for article in articles],
            ["Newer news", "Older news"],
        )
        self.assertEqual(articles[0]["text"], "Newer article")
        self.assertIsNone(articles[0]["icon"])
