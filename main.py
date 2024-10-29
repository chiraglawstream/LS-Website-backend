from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import List, Optional
from pymongo import MongoClient
from datetime import datetime
import re

# Initialize the FastAPI app
app = FastAPI()

# deepakkumar
# PqBVVgNB7UdvqCmT

# Connect to MongoDB
client = MongoClient("mongodb+srv://deepakkumar:PqBVVgNB7UdvqCmT@cluster0.zj3u8.mongodb.net/contact_us_db?retryWrites=true&w=majority&tls=true")
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

# POST API endpoint to handle form submission
@app.post("/contact-us")
async def submit_contact_form(form_data: ContactForm):
    try:
        # Validate phone number format
        validate_phone_number(form_data.phone_number)

        # Debug print to check form data before insertion
        print("Processed form data:", form_data.dict())

        # Insert form data into MongoDB collection
        contact_collection.insert_one(form_data.dict())
        return {"message": "Contact form submitted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit form: {str(e)}")
