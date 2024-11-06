from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import List, Optional
from datetime import datetime

# Pydantic model for validating the form data
class raise_ticket(BaseModel):
    user_id: str
    first_name: str
    email: EmailStr 
    issue: str
    status: str
    created_at: Optional[datetime]

