from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    email = models.EmailField(max_length=254, null=False, blank=False, verbose_name=_('email'))
    message = models.TextField(null=False, blank=False, verbose_name=_('body'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return self.email


class ContactAddress(models.Model):
    address = models.CharField(max_length=250, null=False, blank=False)

    class Meta:
        verbose_name = _('Contact address')
        verbose_name_plural = _('Contact addresses')


class MyPhoneNumbers(models.Model):
    label = models.CharField(max_length=50, null=False, blank=False)
    number = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        verbose_name = _('phone number')
        verbose_name_plural = _('phone numbers')

    def __str__(self):
        return self.label
