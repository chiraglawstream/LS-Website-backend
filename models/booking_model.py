from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import List, Optional
from datetime import datetime

# Pydantic model for validating the form data
class booking_model(BaseModel):
    email: EmailStr 
    tools_of_interest: List[str]
    preferred_demo_datetime: Optional[datetime]
    created_at: Optional[datetime]

