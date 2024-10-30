from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import List, Optional
from pymongo import MongoClient
from datetime import datetime
import re

# Initialize the FastAPI app
app = FastAPI()

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
