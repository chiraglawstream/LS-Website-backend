from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from models.contact_us import ContactForm
from config import configure_cors
from database import get_database
from validators import validate_phone_number
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
        return db["contacts"]  # Ensure this returns the correct collection
    except Exception as e:
        logger.error(f"Failed to get contact collection: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Sanitize the message to remove any HTML or JavaScript code
def sanitize_message(message: str) -> str:
    # Implement or import the sanitize_message function
    # Placeholder sanitization example (assuming `bleach` is installed)
    import bleach
    return bleach.clean(message, strip=True)

# POST API endpoint to handle form submission
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
