import requests

from app.config import settings
from app.models import BookingRequest


BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_confirmation_email(
    booking: BookingRequest,
    to_email: str | None = None,
):
    recipient = to_email or "akshatkutariyar125@gmail.com"

    payload = {
        "sender": {
            "name": "QuensultingAI Dental Clinic",
            "email": "akshatkutariyar125@gmail.com",
        },
        "to": [
            {
                "email": recipient,
            }
        ],
        "subject": f"Appointment Confirmed - {booking.name}",
        "htmlContent": f"""
        <h2>Appointment Confirmation</h2>

        <p>Your appointment has been booked successfully.</p>

        <table border="1" cellpadding="8" cellspacing="0">
            <tr><td><b>Name</b></td><td>{booking.name}</td></tr>
            <tr><td><b>Phone</b></td><td>{booking.phone}</td></tr>
            <tr><td><b>Service</b></td><td>{booking.service}</td></tr>
            <tr><td><b>Date</b></td><td>{booking.date}</td></tr>
            <tr><td><b>Time</b></td><td>{booking.time}</td></tr>
            <tr><td><b>Notes</b></td><td>{booking.notes or "None"}</td></tr>
        </table>

        <br>

        <p>Thank you for choosing QuensultingAI Dental Clinic.</p>
        """,
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.brevo_api_key,
        "content-type": "application/json",
    }

    response = requests.post(
        BREVO_API_URL,
        json=payload,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()