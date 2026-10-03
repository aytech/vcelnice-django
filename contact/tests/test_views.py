import json
from unittest.mock import Mock, patch

from django.test import RequestFactory, TestCase
from django.utils.translation import gettext

from contact.forms import ContactForm
from contact.models import Contact
from contact.views import contact, home


class ContactViewTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    @patch("contact.views.render")
    def test_home_renders_contact_form_for_get(self, render):
        response = object()
        render.return_value = response
        request = self.request_factory.get("/contact/")

        self.assertIs(home(request), response)

        rendered_request, template, context = render.call_args.args
        self.assertIs(rendered_request, request)
        self.assertEqual(template, "contact.html")
        self.assertIsInstance(context["form"], ContactForm)

    def test_home_saves_valid_post(self):
        request = self.request_factory.post(
            "/contact/",
            {"email": "visitor@example.com", "message": "Please contact me"},
        )

        response = home(request)

        self.assertEqual(
            json.loads(response.content),
            {"success": True, "message": None},
        )
        self.assertTrue(
            Contact.objects.filter(
                email="visitor@example.com", message="Please contact me"
            ).exists()
        )

    def test_contact_returns_first_validation_error(self):
        request = self.request_factory.post(
            "/contact/", {"email": "invalid", "message": "Message"}
        )

        response = contact(request)
        payload = json.loads(response.content)

        self.assertFalse(payload["success"])
        self.assertEqual(payload["message"], gettext("Enter a valid email address"))
        self.assertFalse(Contact.objects.exists())

    @patch("contact.views.ContactForm")
    def test_contact_preserves_empty_message_when_invalid_form_has_no_errors(
        self, contact_form
    ):
        form = Mock()
        form.is_valid.return_value = False
        form.errors.as_data.return_value = {}
        contact_form.return_value = form
        request = self.request_factory.post("/contact/")

        response = contact(request)

        self.assertEqual(
            json.loads(response.content),
            {"success": False, "message": None},
        )
        form.save.assert_not_called()
