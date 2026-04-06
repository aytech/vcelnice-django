import base64
import logging
import os
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from django.template.loader import render_to_string

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
