import logging

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

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


@app.post("/api/book-appointment")
async def book_appointment(
    request: Request,
    x_webhook_secret: str | None = Header(default=None),
):
    # Check webhook secret
    if x_webhook_secret != settings.retell_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    # Read raw JSON
    body = await request.json()

    logger.info("=" * 80)
    logger.info("RAW REQUEST BODY:")
    logger.info(body)
    logger.info("=" * 80)

    return {
        "success": True,
        "message": "Request received successfully."
    }