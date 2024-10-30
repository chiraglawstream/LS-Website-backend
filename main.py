<<<<<<< HEAD
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from models.contact_us import ContactForm
from config import configure_cors
from database import get_database
from validators import validate_phone_number
=======
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import List, Optional
from pymongo import MongoClient
from datetime import datetime
import re
>>>>>>> c6264b3c8d07f8a367c44cd3fbf2f6f4c4367d94

# Initialize the FastAPI app
app = FastAPI()

<<<<<<< HEAD
# Configure CORS
configure_cors(app)

# Dependency to get MongoDB collection
def get_contact_collection():
    return get_database()
=======
# chiragyadav
# 9NioCDpLD9OgVt9m
# Configure CORS
origins = [
    "http://localhost:3000",  # Allow requests from localhost for development
    "https://lawstream-web.vercel.app",
    "https://www.lawstream.in"# Add your production frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Connect to MongoDB
client = MongoClient("mongodb+srv://chiragyadav:9NioCDpLD9OgVt9m@cluster0.fptls.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tls=True,
    tlsAllowInvalidCertificates=True)
db = client["contact_us_db"]  # Database name
contact_collection = db["contacts"]  # Collection name

# Function to validate phone numbers
def validate_phone_number(phone: str) -> str:
    phone_regex = re.compile(r'^\+?1?\d{9,15}$')  # Validates phone numbers of 9 to 15 digits, allowing optional country code
    if not phone_regex.match(phone):
        raise ValueError("Invalid phone number format")
    return phone

# Define the Pydantic model for validating the form data
class ContactForm(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: EmailStr  # Email validation
    phone_number: str  # Now this is required
    company_name: str
    job_title: Optional[str]
    subject: str
    tools_of_interest: List[str]
    message: str
    preferred_demo_datetime: Optional[datetime]
>>>>>>> c6264b3c8d07f8a367c44cd3fbf2f6f4c4367d94

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
<<<<<<< HEAD
        raise HTTPException(status_code=500, detail="Failed to submit form due to a server error.")
=======
        raise HTTPException(status_code=500, detail=f"Failed to submit form: {str(e)}")
>>>>>>> c6264b3c8d07f8a367c44cd3fbf2f6f4c4367d94
