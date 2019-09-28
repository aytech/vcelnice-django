# coding=utf-8
from django.core.management.base import BaseCommand
from urllib.parse import unquote_plus
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from contact.models import Contact
from vcelnice.common.gmail import Gmail
import logging
import os, mimetypes

class Command(BaseCommand):
    help = 'Send email collected via contact form'
    LOGGER_NAME = 'vcelnice.info'
    SETTING_NAME = 'DJANGO_SETTINGS_MODULE'
    ENV_DEVELOPMENT = 'vcelnice.settings.development'

    def __init__(self):
        self.logger = logging.getLogger(self.LOGGER_NAME)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        env = os.environ[self.SETTING_NAME]

        if env == self.ENV_DEVELOPMENT:
            from vcelnice.settings import development as settings
        else:
            from vcelnice.settings import production as settings

        gmail = Gmail()
        date_formatted = str(date.today()).replace('-', '_')
        attachments = []

        for filename in os.listdir(settings.LOGS_DIR):
            if date_formatted in filename:
                path = os.path.join(settings.LOGS_DIR, filename)
                attachments.append(dict(name=filename, path=path, type='plain'))
                break

        message_data = dict(
            to=','.join(settings.TO_EMAIL_RECIPIENTS),
            bcc=','.join(settings.BCC_EMAIL_RECIPIENTS),
            sender='Včelnice Rudná',
            subject='Test odeslání e-mailu',
            reply_to=settings.ADMIN_EMAIL_ADDRESS,
            text='''
Toto je automatický test funkčnosti odesílání e-mailů, neodpovídejte prosím
''',
            attachments=attachments,
        )

        if gmail.send_email(message_data):
            self.logger.info('Testovací e-mail byl odeslán')
