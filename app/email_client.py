import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings
from app.models import BookingRequest

logger = logging.getLogger(__name__)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_confirmation_email(
    booking: BookingRequest,
    to_email: str | None = None,
) -> None:
    """
    Sends a booking confirmation email using Gmail SMTP.
    """

    recipient = to_email or settings.gmail_address

    subject = f"Appointment Confirmed - {booking.name}"

    body = f"""
Appointment Confirmation

A new appointment has been booked.

Patient Name: {booking.name}
Phone: {booking.phone}
Service: {booking.service}
Date: {booking.date}
Time: {booking.time}
Notes: {booking.notes or "None"}

This appointment was booked through the AI Voice Receptionist.
"""

    message = MIMEMultipart()
    message["From"] = settings.gmail_address
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        logger.info("Connecting to Gmail SMTP server...")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.starttls()

            logger.info("Logging into Gmail...")

            server.login(
                settings.gmail_address,
                settings.gmail_app_password,
            )

            logger.info("Sending email...")

            server.send_message(message)

        logger.info("Email sent successfully.")

    except Exception:
        logger.exception("Failed to send email.")
        raise