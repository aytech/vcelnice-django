from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Contact, ContactAddress, MyPhoneNumbers


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("email", "message")
        localized_fields = ("email", "message")
        labels = {
            "email": _("Your email address"),
            "message": _("Contact message")
        }
        help_texts = {
            "email": _("Your email address"),
            "message": _("Contact message")
        }
        error_messages = {
            "email": {
                "invalid": _("Enter a valid email address")
            },
            "message": {
                "required": _("Please enter your message")
            }
        }


class ContactAddressForm(forms.ModelForm):
    class Meta:
        model = ContactAddress
        fields = ("address",)


class MyPhoneNumberForm(forms.ModelForm):
    class Meta:
        model = MyPhoneNumbers
        fields = ("label", "number",)
