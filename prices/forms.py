from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("amount", "email", "message", "title", "location")
        error_messages = {
            "sender": {
                "invalid": _("Enter a valid email address"),
                "required": _("Enter a valid email address")
            }
        }
