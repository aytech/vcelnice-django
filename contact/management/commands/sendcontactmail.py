# coding=utf-8
from django.core.management.base import BaseCommand
from urllib.parse import unquote_plus
from contact.models import Contact
from vcelnice.common.gmail import Gmail
import logging
import os


class Command(BaseCommand):
    help = 'Send email collected via contact form'

    def __init__(self):
        self.logger = logging.getLogger('vcelnice.info')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        env = os.environ['DJANGO_SETTINGS_MODULE']

        if env == 'vcelnice.settings.development':
            from vcelnice.settings import development as settings
        else:
            from vcelnice.settings import production as settings

        contact = Contact.objects.filter(deleted=False).first()

        if contact is not None:
            gmail = Gmail()
            message_data = dict(
                text=unquote_plus(contact.message),
                to=','.join(settings.TO_EMAIL_RECIPIENTS),
                bcc=','.join(settings.BCC_EMAIL_RECIPIENTS),
                reply_to=contact.email,
                sender='Včelnice Rudná <%s>' % contact.email,
                subject='Zpráva od návštěvníka webové stránky',
            )

            if gmail.send_email(message_data):
                self.logger.info('Contact email was sent to {0} with text {1}'.format(contact.email, contact.message))
                contact.deleted = True
                contact.save()
