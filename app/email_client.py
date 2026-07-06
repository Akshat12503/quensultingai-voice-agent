import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings
from app.models import BookingRequest


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings
from app.models import BookingRequest

logger = logging.getLogger(__name__)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_confirmation_email(
    booking: BookingRequest,
    to_email: str | None = None,
):
    recipient = to_email or settings.gmail_address

    message = MIMEMultipart()
    message["From"] = settings.gmail_address
    message["To"] = recipient
    message["Subject"] = f"Appointment Confirmed - {booking.name}"

    body = f"""
Patient: {booking.name}
Phone: {booking.phone}
Service: {booking.service}
Date: {booking.date}
Time: {booking.time}
Notes: {booking.notes}
"""

    message.attach(MIMEText(body, "plain"))

    logger.info("Connecting to Gmail...")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=8) as server:

        logger.info("Connected")

        logger.info("Starting TLS...")
        server.starttls()

        logger.info("TLS started")

        logger.info("Logging in...")
        server.login(
            settings.gmail_address,
            settings.gmail_app_password,
        )

        logger.info("Logged in")

        logger.info("Sending email...")

        server.sendmail(
            settings.gmail_address,
            recipient,
            message.as_string(),
        )

        logger.info("Email sent!")