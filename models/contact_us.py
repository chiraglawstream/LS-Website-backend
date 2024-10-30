from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import List, Optional
from datetime import datetime

# Pydantic model for validating the form data
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

