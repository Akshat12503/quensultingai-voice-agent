import requests

from app.config import settings
from app.models import BookingRequest


RESEND_API_URL = "https://api.resend.com/emails"


def send_confirmation_email(
    booking: BookingRequest,
    to_email: str | None = None,
) -> None:
    """
    Sends a booking confirmation email using the Resend API.
    """

    recipient = to_email or settings.gmail_address

    payload = {
        "from": "QuensultingAI Dental Clinic <onboarding@resend.dev>",
        "to": [recipient],
        "subject": f"Appointment Confirmed - {booking.name}",
        "html": f"""
        <h2>Appointment Confirmation</h2>

        <p>A new appointment has been booked.</p>

        <table border="1" cellpadding="8" cellspacing="0">
            <tr>
                <td><b>Name</b></td>
                <td>{booking.name}</td>
            </tr>
            <tr>
                <td><b>Phone</b></td>
                <td>{booking.phone}</td>
            </tr>
            <tr>
                <td><b>Service</b></td>
                <td>{booking.service}</td>
            </tr>
            <tr>
                <td><b>Date</b></td>
                <td>{booking.date}</td>
            </tr>
            <tr>
                <td><b>Time</b></td>
                <td>{booking.time}</td>
            </tr>
            <tr>
                <td><b>Notes</b></td>
                <td>{booking.notes or "None"}</td>
            </tr>
        </table>

        <br>

        <p>This appointment was booked through the AI Voice Receptionist.</p>
        """,
    }

    headers = {
        "Authorization": f"Bearer {settings.resend_api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        RESEND_API_URL,
        json=payload,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()