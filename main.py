from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from models.contact_us import ContactForm
from config import configure_cors
from database import get_database
from validators import validate_phone_number

# Initialize the FastAPI app
app = FastAPI()

# Configure CORS
configure_cors(app)

# Dependency to get MongoDB collection
def get_contact_collection():
    return get_database()

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
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to submit form due to a server error.")
