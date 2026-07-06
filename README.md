# QuensultingAI Dental Clinic - AI Voice Receptionist

An AI-powered voice receptionist built using **Retell AI**, **FastAPI**, **Airtable**, and **Brevo**. The agent handles inbound calls, books appointments, answers common questions, and automates the booking workflow by saving appointments to Airtable and sending confirmation emails.

## Features

- Natural AI voice conversations using Retell AI
- Appointment booking
- Collects patient information
  - Full Name
  - Phone Number
  - Appointment Date
  - Appointment Time
  - Service Requested
  - Additional Notes (Optional)
- Booking confirmation before saving
- Stores appointments in Airtable
- Sends confirmation emails using Brevo
- Handles interruptions and fallback scenarios
- Clean and modular FastAPI backend
- Deployed on Render

---

## Tech Stack

### Voice AI
- Retell AI Conversational Flow

### Backend
- Python
- FastAPI

### Database
- Airtable

### Email Service
- Brevo

### Deployment
- Render

---

## Project Structure

```
quensultingai-voice-agent/
│
├── app/
│   ├── airtable_client.py
│   ├── config.py
│   ├── email_client.py
│   ├── main.py
│   └── models.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Conversation Flow

```
Greeting
      │
      ▼
Identify User Intent
      │
      ▼
Select Service
      │
      ▼
Collect Appointment Date & Time
      │
      ▼
Collect Full Name
      │
      ▼
Collect Phone Number
      │
      ▼
Collect Additional Notes (Optional)
      │
      ▼
Read Booking Summary
      │
      ▼
User Confirmation
      │
      ▼
FastAPI Backend
      │
      ▼
Save Booking to Airtable
      │
      ▼
Send Confirmation Email
      │
      ▼
End Call
```

---

## API Endpoint

### POST

```
/api/book-appointment
```

### Sample Request

```json
{
    "name": "Rahul Kumar",
    "phone": "9876543210",
    "service": "Teeth Whitening",
    "date": "9 July 2026",
    "time": "3:00 PM",
    "notes": "Will arrive 30 minutes early."
}
```

### Sample Response

```json
{
    "success": true,
    "message": "Booking saved and confirmation email sent.",
    "record_id": "recXXXXXXXXXXXX"
}
```

---

## Environment Variables

Create a `.env` file and add the following variables.

```env
AIRTABLE_API_KEY=
AIRTABLE_BASE_ID=
AIRTABLE_TABLE_NAME=Appointments

BREVO_API_KEY=

RETELL_WEBHOOK_SECRET=
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/quensultingai-voice-agent.git
```

Move into the project

```bash
cd quensultingai-voice-agent
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
uvicorn app.main:app --reload
```

---

## Deployment

The backend is deployed using **Render**.

The Retell AI custom function sends appointment data to the deployed FastAPI endpoint, which:

1. Validates the request
2. Saves the booking in Airtable
3. Sends a confirmation email through Brevo
4. Returns a success response to Retell AI

---

## Error Handling

The backend includes error handling for:

- Invalid webhook secret
- Invalid booking payload
- Airtable API failures
- Email delivery failures
- Unexpected server errors

Detailed logging is implemented to simplify debugging and monitoring.

---

## Future Improvements

- Prevent double booking by checking slot availability
- Appointment cancellation and rescheduling
- Google Calendar integration
- SMS and WhatsApp reminders
- Patient email collection
- Staff dashboard for appointment management
- Authentication for clinic administrators

---

## Demo

The project demonstration includes:

- Retell AI conversation flow
- Live appointment booking
- Airtable integration
- Confirmation email
- Backend workflow explanation
- Design decisions
- Challenges and debugging process

---
## Author

**Akshat Kutariyar**
