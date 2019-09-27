from django.contrib import admin

from prices.forms import ReservationForm
from .models import Price, Reservation


class PriceAdmin(admin.ModelAdmin):
    class Meta:
        model = Price


class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm
    list_display = ['title', 'email', 'created', 'deleted']


admin.site.register(Price, PriceAdmin)
admin.site.register(Reservation, ReservationAdmin)
