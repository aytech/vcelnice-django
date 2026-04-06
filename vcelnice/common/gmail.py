# coding=utf-8
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
        message = MIMEMultipart()
        # Headers
        message['to'] = message_data['to']
        message['bcc'] = message_data['bcc']
        message['from'] = message_data['sender']
        message['subject'] = message_data['subject']
        message.add_header('reply-to', message_data['reply_to'])
        # Body
        if 'text' in message_data.keys():
            message.attach(MIMEText(message_data['text'], 'plain'))
        if 'html' in message_data.keys():
            message.attach(MIMEText(message_data['html'], 'html'))
        # Attachments
        if 'attachments' in message_data.keys():
            attachments = message_data['attachments']
            if len(attachments) > 0:
                for data in attachments:
                    with open(data['path']) as file_handler:
                        attachment = MIMEText(file_handler.read(), _subtype=data['type'])
                        attachment.add_header('Content-Disposition', 'attachment', filename=data['name'])
                        message.attach(attachment)

        return base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
