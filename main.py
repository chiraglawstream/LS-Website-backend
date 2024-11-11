from fastapi import FastAPI, HTTPException, Depends, Response
from pydantic import BaseModel, EmailStr
from models.contact_us import ContactForm
from models.chatbot_user_form import chatbot_user_form
from models.raise_ticket import raise_ticket
from models.booking_model import booking_model
from config import configure_cors
from database import get_database
from validators import validate_phone_number
import bleach
import logging
import traceback

# Initialize the FastAPI app
app = FastAPI()

# Configure CORS
configure_cors(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        # Validate phone number format
        validate_phone_number(form_data.phone_number)

        # Sanitize the message to remove any HTML or JS code
        sanitized_message = sanitize_message(form_data.message)
        
        # Prepare sanitized form data for MongoDB insertion
        sanitized_data = form_data.dict()
        sanitized_data["message"] = sanitized_message  # Replace message with sanitized message

        # Insert form data into MongoDB collection
        contact_collection.insert_one(sanitized_data)
        return {"message": "Contact form submitted successfully."}
    
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        # Log the detailed stack trace
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
         # Validate phone number format
        validate_phone_number(form_data.phone_number)

        # Insert form data into MongoDB collection
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

        # Sanitize the message to remove any HTML or JS code
        sanitized_data = ticket_data.dict()
        sanitized_data["issue"] = sanitized_message 

        # Insert form data into MongoDB collection
        chatbot_user_ticket.insert_one(sanitized_data)

        return {
            "message": "Ticket raised successfully.",
        }
    
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        # Log the detailed stack trace
        logger.error(f"Internal server error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to raise ticket due to a server error.")


# POST API endpoint to handle chatbot bookings submission
@app.post("/booking")
async def submit_chatbot_user_booking(
    booking_data: booking_model, 
    chatbot_user_booking=Depends(get_chatbot_user_booking)
):
    try:

        # Insert booking data into MongoDB collection
        chatbot_user_booking.insert_one(booking_data.dict())

        return {
            "message": "Appointed booked successfully.",
        }
    
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        # Log the detailed stack trace
        logger.error(f"Internal server error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to book appointment due to a server error.")
