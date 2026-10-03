from django.test import TestCase
from django.urls import reverse

from documents.models import Certificate


class CertificateAPIViewTests(TestCase):
    def test_api_root_links_to_certificate_list(self):
        response = self.client.get(reverse("certificates-api:root"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(
            response.json(),
            {
                "certificates": (
                    "http://testserver"
                    + reverse("certificates-api:certificates-list")
                )
            },
        )

    def test_certificate_list_serializes_available_certificates(self):
        Certificate.objects.create(
            description="Beekeeping certificate",
            file="documents/certificate.pdf",
        )

        response = self.client.get(reverse("certificates-api:certificates-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(
            response.json(),
            {
                "certificates": [
                    {
                        "description": "Beekeeping certificate",
                        "file": "/media/documents/certificate.pdf",
                        "type": "application/pdf",
                    }
                ]
            },
        )
