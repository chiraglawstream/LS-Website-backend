from fastapi import FastAPI, HTTPException, Depends, Response
from pydantic import BaseModel, EmailStr
from models.contact_us import ContactForm
from models.chatbot_user_form import chatbot_user_form
from models.raise_ticket import raise_ticket
from models.booking_model import booking_model
from scripts.email_sender import send_email
from config import configure_cors
from database import get_database
from validators import validate_phone_number
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib
import os
import bleach
import logging
import traceback

app = FastAPI()

# Configure CORS
configure_cors(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email Sender function
def send_email(to_email: str, subject: str, body: str, cc_email: str = None):
    try:
        load_dotenv()
        from_email = "teamlawstream@gmail.com"
        password = "tpqo jqaj ozmi fotm"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        if cc_email:
            msg["Cc"] = cc_email

        msg.attach(MIMEText(body, "plain"))

        server.sendmail(from_email, [to_email] + ([cc_email] if cc_email else []), msg.as_string())

        server.quit()

    except Exception as e:
        logger.error(f"Failed to send email: {traceback.format_exc()}")

# Dependency to get MongoDB collection
def get_contact_collection():
    try:
        db = get_database()
        return db["contacts"]
    except Exception as e:
        logger.error(f"Failed to get contact collection: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Database connection error")


# Dependency to get MongoDB collection for chatbor form
def get_chatbot_user_collection():
    try:
        db = get_database()
        return db["chatbot_user_form"]
    except Exception as e:
        logger.error(f"Failed to get contact collection: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Dependency to get MongoDB collection for ticket
def get_chatbot_user_ticket():
    try:
        db = get_database()
        return db["chatbot_user_ticket"]
    except Exception as e:
        logger.error(f"Failed to get contact collection: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Dependency to get MongoDB collection for ticket
def get_chatbot_user_booking():
    try:
        db = get_database()
        return db["chatbot_user_booking"]
    except Exception as e:
        logger.error(f"Failed to get contact collection: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Sanitize the message to remove any HTML or JavaScript code
def sanitize_message(message: str) -> str:
    return bleach.clean(message, strip=True)

# POST API endpoint to handle contact form submission
@app.post("/contact-us")
async def submit_contact_form(
    form_data: ContactForm, 
    contact_collection=Depends(get_contact_collection)
):
    try:
        validate_phone_number(form_data.phone_number)

        sanitized_message = sanitize_message(form_data.message)
        
        sanitized_data = form_data.dict()
        sanitized_data["message"] = sanitized_message

        contact_collection.insert_one(sanitized_data)
        return {"message": "Contact form submitted successfully."}
    
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        logger.error(f"Internal server error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to submit form due to a server error.")


# POST API endpoint to handle chatbot form submission
@app.post("/chatbot")
async def submit_chatbot_user_form(
    form_data: chatbot_user_form, 
    response : Response,
    chatbot_user_collection=Depends(get_chatbot_user_collection)
):
    try:
        validate_phone_number(form_data.phone_number)

        chatbot_user_collection.insert_one(form_data.dict())

        return {
            "message": "Chatbot form submitted successfully.",
        }
    
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        # Log the detailed stack trace
        logger.error(f"Internal server error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to submit form due to a server error.")



# POST API endpoint to handle chatbot ticket submission
@app.post("/ticket")
async def submit_chatbot_user_ticket(
    ticket_data: raise_ticket, 
    chatbot_user_ticket=Depends(get_chatbot_user_ticket)
):
    try:
        sanitized_message = sanitize_message(ticket_data.issue)
        sanitized_data = ticket_data.dict()
        sanitized_data["issue"] = sanitized_message 

        chatbot_user_ticket.insert_one(sanitized_data)

        subject = "New Support Ticket Raised"
        body = f"Issue: {ticket_data.issue}\nStatus: {ticket_data.status}"
        to_email = "Support@lawstream.in" 
        cc_email = ticket_data.email

        try:
            send_email(to_email=to_email, subject=subject, body=body, cc_email=cc_email)
        except Exception as email_error:
            logger.error(f"Failed to send email: {email_error}")
            raise HTTPException(status_code=500, detail="Ticket created, but failed to send notification email.")

        return {
            "message": "Ticket raised successfully.",
        }
    
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        logger.error(f"Internal server error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to raise ticket due to a server error.")


# POST API endpoint to handle chatbot bookings submission
@app.post("/booking")
async def submit_chatbot_user_booking(
    booking_data: booking_model, 
    chatbot_user_booking=Depends(get_chatbot_user_booking)
):
    try:

        chatbot_user_booking.insert_one(booking_data.dict())

        subject = "New Booking Appointment Created"
        body = (
            f"Tools of Interest: {', '.join(booking_data.tools_of_interest)}\n"
            f"Preferred Demo DateTime: {booking_data.preferred_demo_datetime}"
        )
        to_email = "Support@lawstream.in"  
        cc_email = booking_data.email

        try:
            send_email(to_email=to_email, subject=subject, body=body, cc_email=cc_email)
        except Exception as email_error:
            logger.error(f"Failed to send email: {email_error}")
            raise HTTPException(status_code=500, detail="Ticket created, but failed to send notification email.")

        return {
            "message": "Appointement booked successfully.",
        }
    
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        logger.error(f"Internal server error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to book appointment due to a server error.")

