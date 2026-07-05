import logging

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import BookingRequest, BookingResponse
from app.airtable_client import save_booking_to_airtable
from app.email_client import send_confirmation_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("quensultingai-voice-agent")

app = FastAPI(title="QuensultingAI Dental Clinic Voice Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "quensultingai-voice-agent"}


@app.post("/api/book-appointment", response_model=BookingResponse)
def book_appointment(
    booking: BookingRequest,
    x_webhook_secret: str | None = Header(default=None),
):
    # Basic auth check so random callers can't hit our webhook
    if x_webhook_secret != settings.retell_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    logger.info(f"Received booking request for {booking.name} - {booking.service}")

    # Step 1: Save to Airtable
    try:
        record_id = save_booking_to_airtable(booking)
        logger.info(f"Saved booking to Airtable with record ID {record_id}")
    except Exception as e:
        logger.error(f"Airtable save failed: {e}")
        raise HTTPException(
            status_code=502,
            detail="Failed to save booking. Please transfer caller to staff.",
        )

    # Step 2: Send confirmation email (non-fatal if it fails)
    try:
        send_confirmation_email(booking)
        logger.info("Confirmation email sent")
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        # We don't fail the whole request if only the email fails -
        # the booking itself was already saved successfully.
        return BookingResponse(
            success=True,
            message="Booking saved, but confirmation email failed to send.",
            record_id=record_id,
        )

    return BookingResponse(
        success=True,
        message="Booking saved and confirmation email sent.",
        record_id=record_id,
    )