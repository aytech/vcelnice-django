from django.test import TestCase

from contact.models import Contact, MyPhoneNumbers


class ContactModelTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(email="oyapparov@gmail.com", message="Test Contact")

    def test_contact_created(self):
        contact = Contact.objects.get()
        self.assertFalse(contact.deleted)
        self.assertEqual("Test Contact", contact.message)
        self.assertEqual(str(contact), "oyapparov@gmail.com")

    def test_phone_number_uses_label_as_string(self):
        phone_number = MyPhoneNumbers(label="Mobile", number="+420123456789")

        self.assertEqual(str(phone_number), "Mobile")
