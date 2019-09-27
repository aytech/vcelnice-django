# coding=utf-8
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
from oauth2client.file import Storage
from apiclient import discovery
import httplib2
import logging
import os


class Gmail:
    APPLICATION_NAME = 'Včelnice Rudná'
    CLIENT_SECRET_FILE = 'gmail-python-vcelnice.json'
    CREDENTIALS_DIR = '.credentials'
    GMAIL_API_SERVICE_NAME = 'gmail'
    GMAIL_API_VERSION = 'v1'

    def __init__(self):
        self.logger = logging.getLogger('vcelnice.info')

    @staticmethod
    def create_text_email(message_data):
        message = MIMEMultipart('alternative')
        # Headers
        message['to'] = message_data['to']
        message['bcc'] = message_data['bcc']
        message['from'] = message_data['sender']
        message['subject'] = message_data['subject']
        message.add_header('reply-to', message_data['reply_to'])
        # Body
        message.attach(MIMEText(message_data['text'], 'plain'))
        message.attach(MIMEText(message_data['text'], 'html'))

        return base64.urlsafe_b64encode(message.as_bytes())

    def get_credentials(self):
        cred_dir = os.path.dirname(os.path.abspath(__file__))
        credential_dir = os.path.join(cred_dir, self.CREDENTIALS_DIR)
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, self.CLIENT_SECRET_FILE)

        store = Storage(credential_path)
        return store.get()

    def send_email(self, message_data):
        message_encoded = self.create_text_email(message_data)
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build(self.GMAIL_API_SERVICE_NAME, self.GMAIL_API_VERSION, http=http)

        try:
            message = (service.users().messages().send(userId='me', body={'raw': message_encoded.decode()})
                       .execute())
            self.logger.info('Message was sent with ID %s' % message['id'])
            return True
        except HttpError as error:
            self.logger.critical('Error sending email: %s' % error)

        return False
