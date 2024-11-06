from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import List, Optional
from datetime import datetime

# Pydantic model for validating the chatbot form data
class chatbot_user_form(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: EmailStr  # Email validation
    phone_number: str  
    company_name: str
    job_title: Optional[str]    
