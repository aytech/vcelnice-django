from django.db import models
from django.utils.translation import gettext_lazy as _

from vcelnice.common.model import Model


class Contact(Model):
    email = models.EmailField(max_length=254, null=False, blank=False, verbose_name=_("Email"))
    id = models.BigAutoField(primary_key=True)
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
    id = models.BigAutoField(primary_key=True)

    class Meta:
        verbose_name = _("Contact address")
        verbose_name_plural = _("Contact addresses")


class MyPhoneNumbers(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=50, null=False, blank=False, verbose_name=_("Label"))
    number = models.CharField(max_length=50, null=False, blank=False, verbose_name=_("Number"))

    class Meta:
        verbose_name = _("Phone number")
        verbose_name_plural = _("Phone numbers")

    def __str__(self):
        return self.label
