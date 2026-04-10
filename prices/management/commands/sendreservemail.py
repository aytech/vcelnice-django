# coding=utf-8
import logging
from urllib.parse import unquote_plus

from django.conf import settings
from django.core.management.base import BaseCommand

from prices.models import Reservation
from vcelnice.common.gmail import Gmail


class Command(BaseCommand):
    help = 'Send reservation emails'
    LOGGER_NAME = 'vcelnice.info'

    def __init__(self):
        self.logger = logging.getLogger(self.LOGGER_NAME)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        reservation = Reservation.objects.filter(deleted=False).first()

        if reservation is not None:
            gmail = Gmail()
            message_data = dict(
                html='''
<strong>
    Položka:
</strong> {0}<br/>
<strong>
    Pocet:
</strong> {1}<br/>
<strong>
    Poznámka:
</strong> {2}<br/>
<strong>
    Vyzvednutí:
</strong> {3}             
'''.format(
                    reservation.title, reservation.amount, unquote_plus(reservation.message),
                    'Nespecifikováno' if reservation.location is None else reservation.location
                ),
                to=','.join(settings.TO_EMAIL_RECIPIENTS),
                bcc=','.join(settings.BCC_EMAIL_RECIPIENTS),
                reply_to=reservation.email,
                sender='Včelnice Rudná - Rezervace <%s>' % reservation.email,
                subject='Rezervace medu',
            )

            if gmail.send_email(message_data):
                self.logger.info(
                    'Message from {0} was sent with message {1}'.format(reservation.email, reservation.message))
                reservation.deleted = True
                reservation.save()
