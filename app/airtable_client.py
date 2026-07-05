import requests
from app.config import settings
from app.models import BookingRequest


AIRTABLE_API_URL = (
    f"https://api.airtable.com/v0/{settings.airtable_base_id}/{settings.airtable_table_name}"
)


def save_booking_to_airtable(booking: BookingRequest) -> str:
    """
    Saves a booking record to Airtable.
    Returns the created record ID.
    Raises requests.HTTPError on failure.
    """
    headers = {
        "Authorization": f"Bearer {settings.airtable_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "fields": {
            "Name": booking.name,
            "Phone": booking.phone,
            "Service": booking.service,
            "Appointment Date": booking.date,
            "Appointment Time": booking.time,
            "Notes": booking.notes or "",
            "Status": "Confirmed",
        }
    }

    response = requests.post(AIRTABLE_API_URL, json=payload, headers=headers, timeout=10)

    if not response.ok:
        print("AIRTABLE ERROR RESPONSE:", response.status_code, response.text)

    response.raise_for_status()

    data = response.json()
    return data["id"]