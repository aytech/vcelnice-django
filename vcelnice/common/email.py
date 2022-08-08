import logging
import os

from python_http_client import HTTPError
from sendgrid import SendGridAPIClient, Mail, Personalization, To, Bcc

from vcelnice.serializers.ContactSerializer import ContactSerializer


class Email:
    def __init__(self):
        env = os.environ['DJANGO_SETTINGS_MODULE']
        if env == 'vcelnice.settings.production':
            from vcelnice.settings import production as configuration
        else:
            from vcelnice.settings import development as configuration
        self.configuration = configuration

    def send_contact_email(self, data: ContactSerializer):
        mail = Mail(from_email=(self.configuration.SENDER_EMAIL_ADDRESS, self.configuration.SENDER_EMAIL_NAME))
        personalization = Personalization()
        for recipient in self.configuration.TO_EMAIL_RECIPIENTS:
            personalization.add_email(To(recipient['address']))
        for bcc in self.configuration.BCC_EMAIL_RECIPIENTS:
            personalization.add_email(Bcc(bcc['address']))
        mail.add_personalization(personalization)
        mail.reply_to = data.data.get('email')
        mail.dynamic_template_data = {
            'email': data.data.get('email'),
            'message': data.data.get('message')
        }
        mail.template_id = os.environ['EMAIL_CONTACT_TEMPLATE']
        try:
            SendGridAPIClient(os.environ['EMAIL_API_KEY']).send(mail)
        except HTTPError as e:
            logging.getLogger('vcelnice.info').error(e.to_dict)
