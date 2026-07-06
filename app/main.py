import logging

from fastapi import FastAPI, Header, HTTPException, Request
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
async def book_appointment(
    request: Request,
    x_webhook_secret: str | None = Header(default=None),
):
    # Verify Retell webhook secret
    if x_webhook_secret != settings.retell_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    # Read request body
    body = await request.json()

    logger.info("=" * 80)
    logger.info("RAW REQUEST BODY:")
    logger.info(body)
    logger.info("=" * 80)

    # Support both Retell payload formats
    booking_data = body.get("args", body)

    try:
        booking = BookingRequest(**booking_data)
    except Exception as e:
        logger.exception("Invalid booking payload")
        raise HTTPException(status_code=400, detail="Invalid booking payload")

    logger.info(
        f"Received booking request for {booking.name} - {booking.service}"
    )

    # Save booking to Airtable
    try:
        record_id = save_booking_to_airtable(booking)
        logger.info(
            f"Saved booking to Airtable with record ID {record_id}"
        )
    except Exception:
        logger.exception("Airtable save failed")
        raise HTTPException(
            status_code=502,
            detail="Failed to save booking.",
        )

    # Send confirmation email
    try:
        logger.info("Sending confirmation email...")

        send_confirmation_email(booking)

        logger.info("Confirmation email sent successfully.")

    except Exception:
        logger.exception("Email sending failed")

        return BookingResponse(
            success=True,
            message="Booking saved successfully, but confirmation email failed.",
            record_id=record_id,
        )

    return BookingResponse(
        success=True,
        message="Booking saved and confirmation email sent.",
        record_id=record_id,
    )