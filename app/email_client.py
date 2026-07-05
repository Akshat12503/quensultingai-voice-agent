import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings
from app.models import BookingRequest


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_confirmation_email(booking: BookingRequest, to_email: str | None = None) -> None:
    """
    Sends a booking confirmation email.
    If `to_email` is not provided, sends the notification to the clinic's own inbox
    (since the voice agent typically only collects a phone number, not an email).
    Raises smtplib.SMTPException on failure.
    """
    recipient = to_email or settings.gmail_address

    subject = f"Appointment Confirmed - {booking.name} - {booking.service}"
    body = f"""
A new appointment has been booked at QuensultingAI Dental Clinic.

Patient Name: {booking.name}
Phone: {booking.phone}
Service: {booking.service}
Date: {booking.date}
Time: {booking.time}
Notes: {booking.notes or "None"}

This booking was made via the AI receptionist voice agent.
""".strip()

    message = MIMEMultipart()
    message["From"] = settings.gmail_address
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(settings.gmail_address, settings.gmail_app_password)
        server.sendmail(settings.gmail_address, recipient, message.as_string())