import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from documents.models import Certificate


class CertificateModelTests(TestCase):
    def test_save_sets_type_for_supported_documents(self):
        document_types = {
            ".pdf": "application/pdf",
            ".doc": "application/msword",
        }

        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            for extension, content_type in document_types.items():
                with self.subTest(extension=extension):
                    certificate = Certificate(
                        description=f"Certificate {extension}",
                        file=SimpleUploadedFile(
                            f"certificate{extension}", b"document-content"
                        ),
                    )

                    certificate.save()
                    certificate.refresh_from_db()

                    self.assertEqual(certificate.type, content_type)
                    self.assertEqual(str(certificate), f"Certificate {extension}")
                    self.assertTrue(
                        certificate.file.storage.exists(certificate.file.name)
                    )
