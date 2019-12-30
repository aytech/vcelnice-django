from django.db import models
from django.utils.translation import ugettext_lazy as _
from vcelnice.common.image import ImageUploader


class Reservation(models.Model):
    amount = models.IntegerField(default=1, null=False, blank=False, verbose_name=_("Amount"))
    email = models.EmailField(null=False, blank=False, verbose_name=_("Email"))
    message = models.TextField(null=True, blank=True, verbose_name=_("Message"))
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Title"))
    location = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Location"))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_("Created"))
    deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")


class Price(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("Title"))
    price = models.IntegerField(null=False, blank=False, verbose_name=_("Price"))
    weight = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Weight"))
    in_store = models.IntegerField(default=0, blank=False, null=False, verbose_name=_("In store"))
    amount_description = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Amount description"),
                                          help_text=_("Description of amount for reservation, e.g. Number of glasses"))
    image = models.ImageField(upload_to='prices/', max_length=100, null=False, blank=False, verbose_name=_("Image"))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.image:
            price = Price.objects.filter(image=self.image)
            if len(price) == 0:
                uploader = ImageUploader(self.image)
                uploader.save_model(self)

        super(Price, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Price")
        verbose_name_plural = _("Prices")
