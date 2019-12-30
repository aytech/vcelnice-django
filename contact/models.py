from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    email = models.EmailField(max_length=254, null=False, blank=False, verbose_name=_("Email"))
    message = models.TextField(null=False, blank=False, verbose_name=_("Message"))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_("Created"))
    deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return self.email


class ContactAddress(models.Model):
    objects = models.Manager()
    address = models.CharField(max_length=250, null=False, blank=False, verbose_name=_("Address"))

    class Meta:
        verbose_name = _("Contact address")
        verbose_name_plural = _("Contact addresses")


class MyPhoneNumbers(models.Model):
    label = models.CharField(max_length=50, null=False, blank=False, verbose_name=_("Label"))
    number = models.CharField(max_length=50, null=False, blank=False, verbose_name=_("Number"))

    class Meta:
        verbose_name = _("Phone number")
        verbose_name_plural = _("Phone numbers")

    def __str__(self):
        return self.label
