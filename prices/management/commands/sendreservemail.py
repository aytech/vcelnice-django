# coding=utf-8
from django.core.management.base import BaseCommand
from urllib.parse import unquote_plus
from prices.models import Reservation
from vcelnice.common.gmail import Gmail
import os


class Command(BaseCommand):
    help = 'Send reservation emails'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        env = os.environ['DJANGO_SETTINGS_MODULE']

        if env == 'vcelnice.settings.development':
            from vcelnice.settings import development as settings
        else:
            from vcelnice.settings import production as settings

        reservation = Reservation.objects.filter(deleted=False).first()

        if reservation is not None:
            gmail = Gmail()
            message_data = dict(
                text='<strong>Položka:</strong> %s<br/><strong>Pocet:</strong> %i<br/><strong>Poznámka:</strong> '
                     '%s<br/><strong>Vyzvednutí:</strong> %s' % (
                         reservation.title,
                         reservation.amount,
                         unquote_plus(reservation.message),
                         'Nespecifikováno' if reservation.location is None else reservation.location
                     ),
                to=','.join(settings.TO_EMAIL_RECIPIENTS),
                bcc=','.join(settings.BCC_EMAIL_RECIPIENTS),
                reply_to=reservation.email,
                sender='Včelnice Rudná - Rezervace <%s>' % reservation.email,
                subject='Rezervace medu',
            )

            if gmail.send_email(message_data):
                reservation.deleted = True
                reservation.save()
