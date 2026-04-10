from django.test import TestCase

from contact.models import Contact


class ContactModelTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(email="oyapparov@gmail.com", message="Test Contact")

    def test_contact_created(self):
        contact = Contact.objects.get(email="oyapparov@gmail.com")
        self.assertFalse(contact.deleted)
        self.assertEqual("Test Contact", contact.message)
