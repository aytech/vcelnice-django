from django.test import TestCase
from django.urls import reverse

from prices.models import Price


class PricesAPIViewTests(TestCase):
    def test_api_root_links_to_prices_list(self):
        response = self.client.get(reverse("prices-api:root"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(
            response.json(),
            {"prices": "http://testserver" + reverse("prices-api:prices-list")},
        )

    def test_prices_list_serializes_available_prices(self):
        price = Price.objects.bulk_create(
            [
                Price(
                    title="Honey",
                    price=200,
                    weight="950 g",
                    in_store=12,
                    amount_description="Number of glasses",
                    image="prices/honey.jpg",
                )
            ]
        )[0]

        response = self.client.get(reverse("prices-api:prices-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(
            response.json(),
            {
                "prices": [
                    {
                        "id": price.pk,
                        "title": "Honey",
                        "price": 200,
                        "weight": "950 g",
                        "in_store": 12,
                        "amount_description": "Number of glasses",
                        "image": "/media/prices/honey.jpg",
                    }
                ]
            },
        )
