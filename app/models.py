from typing import Optional
from pydantic import BaseModel, Field


class BookingRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Caller's full name")
    phone: str = Field(..., min_length=1, description="Caller's phone number")
    service: str = Field(..., min_length=1, description="Requested dental service")
    date: str = Field(..., min_length=1, description="Requested appointment date")
    time: str = Field(..., min_length=1, description="Requested appointment time")
    notes: Optional[str] = Field(default="", description="Additional notes from caller")


class BookingResponse(BaseModel):
    success: bool
    message: str
    record_id: Optional[str] = None