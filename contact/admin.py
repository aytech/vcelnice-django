from django.contrib import admin

from contact.forms import ContactForm, ContactAddressForm, MyPhoneNumberForm
from contact.models import Contact, ContactAddress, MyPhoneNumbers


class ContactAdmin(admin.ModelAdmin):
    form = ContactForm
    list_display = ['email', 'created', 'deleted']


class ContactAddressAdmin(admin.ModelAdmin):
    form = ContactAddressForm
    list_display = ['address', ]


class MyPhoneNumbersAdmin(admin.ModelAdmin):
    form = MyPhoneNumberForm
    fields = ['label', 'number', ]
    list_display = ['label', 'number', ]

    class Meta:
        verbose_name = "Phone"
        verbose_name_plural = "Phone"


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactAddress, ContactAddressAdmin)
admin.site.register(MyPhoneNumbers, MyPhoneNumbersAdmin)
