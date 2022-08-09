import logging
import os

from python_http_client import HTTPError
from sendgrid import SendGridAPIClient, Mail, Personalization, To, Bcc

from vcelnice.serializers.ContactSerializer import ContactSerializer
from vcelnice.serializers.ReservationSerializer import ReservationSerializer


class Email:
    def __init__(self):
        env = os.getenv('DJANGO_SETTINGS_MODULE')
        if env == 'vcelnice.settings.production':
            from vcelnice.settings import production as configuration
        else:
            from vcelnice.settings import development as configuration
        self.configuration = configuration

    def send_contact_email(self, data: ContactSerializer):
        mail = self.get_email_template()
        mail.reply_to = data.data.get('email')
        mail.dynamic_template_data = {
            'email': data.data.get('email'),
            'message': data.data.get('message')
        }
        mail.template_id = os.getenv('EMAIL_CONTACT_TEMPLATE')
        self.send_email(mail)

    def send_reservation_email(self, data: ReservationSerializer):
        mail = self.get_email_template()
        mail.reply_to = data.data.get('email')
        mail.dynamic_template_data = {
            'count': data.data.get('amount'),
            'item': data.data.get('title'),
            'location': data.data.get('location'),
            'note': data.data.get('message'),
            'sender': data.data.get('email')
        }
        mail.template_id = os.getenv('EMAIL_RESERVATION_TEMPLATE')
        self.send_email(mail)

    def get_email_template(self):
        mail = Mail(from_email=(self.configuration.SENDER_EMAIL_ADDRESS, self.configuration.SENDER_EMAIL_NAME))
        personalization = Personalization()
        for recipient in self.configuration.TO_EMAIL_RECIPIENTS:
            personalization.add_email(To(recipient['address']))
        for bcc in self.configuration.BCC_EMAIL_RECIPIENTS:
            personalization.add_email(Bcc(bcc['address']))
        mail.add_personalization(personalization)
        return mail

    @staticmethod
    def send_email(email: Mail):
        try:
            SendGridAPIClient(os.getenv('EMAIL_API_KEY')).send(email)
        except HTTPError as e:
            logging.getLogger('vcelnice.info').error(e.to_dict)
