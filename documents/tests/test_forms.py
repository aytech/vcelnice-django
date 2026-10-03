from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from documents.forms import DocumentForm


class DocumentFormTests(SimpleTestCase):
    def test_accepts_supported_document_extensions(self):
        for extension in (".pdf", ".doc"):
            with self.subTest(extension=extension):
                uploaded_file = SimpleUploadedFile(
                    f"certificate{extension}", b"document-content"
                )
                form = DocumentForm(
                    data={"description": "Certificate"},
                    files={"file": uploaded_file},
                )

                self.assertTrue(form.is_valid(), form.errors)
                self.assertIs(form.cleaned_data["file"], uploaded_file)

    def test_rejects_unsupported_document_extension(self):
        form = DocumentForm(
            data={"description": "Certificate"},
            files={
                "file": SimpleUploadedFile("certificate.txt", b"document-content")
            },
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["file"],
            ["Invalid file, please upload only .PDF or .DOC files"],
        )
