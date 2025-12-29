import base64
import logging
import os
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from django.template.loader import render_to_string
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from prices.models import Reservation
from vcelnice.serializers.ContactSerializer import ContactSerializer
from vcelnice.serializers.ReservationSerializer import ReservationSerializer


class EmailException(Exception):
    pass


class Email:
    def __init__(self):
        env = os.getenv('DJANGO_SETTINGS_MODULE')
        if env == 'vcelnice.settings.production':
            from vcelnice.settings import production as configuration
        else:
            from vcelnice.settings import development as configuration
        self.configuration = configuration
        self.logger = logging.getLogger("vcelnice.info")
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
        self.service = self.authenticate_gmail()

    def authenticate_gmail(self):
        credentials = None
        token_path = self.configuration.BASE_DIR + "/common/credentials/token.json"
        try:
            credentials = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        except FileNotFoundError:
            self.logger.info("Credentials file not found")
        except Exception as e:
            self.logger.info("Unexpected error trying to authenticate with Gmail: ", e)

        if not credentials or not credentials.valid:
            self.logger.info("Credentials are not valid, authenticate")
            return None
            # creds_path = self.configuration.BASE_DIR + "/common/credentials/credentials.json"
            # flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.SCOPES)
            # creds = flow.run_local_server(port=0)

            with open(token_path, "w") as token:
                token.write(creds.to_json())

        return build("gmail", "v1", credentials=credentials)

    @staticmethod
    def formataddr_utf8(sender: str, email: str) -> str:
        """
        Returns an RFC-compliant email address with UTF-8 display name.
        Example: José Pérez <jose@example.com>
        """
        # Header encodes UTF-8 characters safely
        return formataddr((Header(sender, 'utf-8').encode(), email))

    def send_contact_email(self, data: ContactSerializer):
        self.logger.info("send_contact_email is to be implemented")
        # mail = self.get_email_template()
        # mail.reply_to = data.data.get('email')
        # mail.dynamic_template_data = {
        #     'email': data.data.get('email'),
        #     'message': data.data.get('message')
        # }
        # mail.template_id = os.getenv('EMAIL_CONTACT_TEMPLATE')
        # self.send_email(mail)

    def send_reservation_email(self, data: ReservationSerializer):
        if self.service is None:
            return

        message = MIMEMultipart("alternative")
        message["From"] = self.formataddr_utf8(self.configuration.SENDER_EMAIL_NAME,
                                               self.configuration.SENDER_EMAIL_ADDRESS)
        message["To"] = ", ".join(
            self.formataddr_utf8(sender, email) for sender, email in self.configuration.TO_EMAIL_RECIPIENTS)
        message["Bcc"] = ", ".join(
            formataddr((sender, email)) for sender, email in self.configuration.BCC_EMAIL_RECIPIENTS)
        message["Subject"] = "Rezervace medu"

        html_body = render_to_string("email/reservation.html", context={
            "item": data.data.get("title"),
            "count": data.data.get("amount"),
            "note": data.data.get("message") or "",
            "location": data.data.get("location"),
            "sender": data.data.get("email")
        })

        message.attach(MIMEText("Please view this email in HTML.", "plain"))
        message.attach(MIMEText(html_body, "html"))

        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        send_body = {"raw": raw_message}

        result = self.service.users().messages().send(
            userId="me",
            body=send_body
        ).execute()

        reservation = Reservation.objects.get(id=data.data.get("id"))
        reservation.deleted = True
        reservation.save()

        self.logger.info(f"Email sent. Message ID: {result['id']}")

    def send_email(self, email):
        self.logger.info("send_email is to be implemented")
        # try:
        #     SendGridAPIClient(os.getenv('EMAIL_API_KEY')).send(email)
        # except HTTPError as e:
        #     logging.getLogger('vcelnice.info') \
        #         .error(
        #         'Failed to send email from {}, error: {}, API key: {}'.format(
        #             email.dynamic_template_data['sender'], e.to_dict, os.getenv('EMAIL_API_KEY')
        #         ))
        #     raise EmailException
        # except Exception as e:
        #     logging.getLogger('vcelnice.info') \
        #         .error(
        #         'Failed to send email from {}, error: {}, API key: {}'.format(
        #             email.dynamic_template_data['sender'], e, os.getenv('EMAIL_API_KEY')
        #         ))
        #     raise EmailException
