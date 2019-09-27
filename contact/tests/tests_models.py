from django.test import TestCase
from contact.models import Contact


class ContactModelTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(visitor='oyapparov@gmail.com', body='Test Contact')

    def test_contact_created(self):
        contact = Contact.objects.get(visitor='oyapparov@gmail.com')
        self.assertFalse(contact.deleted)
